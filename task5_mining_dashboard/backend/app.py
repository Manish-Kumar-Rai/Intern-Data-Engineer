import os
import io
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from aiohttp import ClientSession
from dotenv import load_dotenv
from analysis import series_stats, anomalies_iqr, anomalies_zscore, anomalies_ma_pct, grubbs_test, poly_fit, poly_predict
import pyppeteer
from jinja2 import Template

load_dotenv()
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL")
if not SHEET_CSV_URL:
    raise RuntimeError("SHEET_CSV_URL not set in env")

app = FastAPI(title="Mining Dashboard API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Fetch CSV -------------------
async def fetch_sheet():
    async with ClientSession() as sess:
        async with sess.get(SHEET_CSV_URL) as r:
            if r.status != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch sheet")
            txt = await r.text()
    df = pd.read_csv(io.StringIO(txt))
    df.columns = df.columns.str.strip()
    if "Date" not in df.columns:
        raise HTTPException(status_code=500, detail="Date column missing in sheet")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).reset_index(drop=True)
    return df

@app.get("/")
def home():
    return {"status": "OK"}


# ------------------- API: /data -------------------
@app.get("/api/data")
async def get_data():
    df = await fetch_sheet()
    return {
        "dates": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "mines": {c: df[c].fillna(np.nan).tolist() for c in df.columns if c != "Date"}
    }

# ------------------- API: /analyze -------------------
@app.post("/api/analyze")
async def analyze(payload: dict):
    params = payload.get("params", {})
    iqr_k = float(params.get("iqr_k", 1.5))
    z_thresh = float(params.get("z_thresh", 3.0))
    ma_window = int(params.get("ma_window", 7))
    ma_pct = float(params.get("ma_pct", 0.3))
    grubbs_alpha = float(params.get("grubbs_alpha", 0.05))
    trend_degree = int(params.get("trend_degree", 1))

    df = await fetch_sheet()
    dates = df["Date"].dt.strftime("%Y-%m-%d").tolist()
    mines = {}
    total_series = np.zeros(len(df))

    for c in df.columns:
        if c == "Date":
            continue
        series = df[c].astype(float).tolist()
        total_series += np.nan_to_num(np.array(series))
        stats = series_stats(series)
        mines[c] = {
            "stats": stats,
            "iqr": anomalies_iqr(series, k=iqr_k),
            "z": anomalies_zscore(series, thresh=z_thresh),
            "ma_pct": anomalies_ma_pct(series, window=ma_window, pct=ma_pct),
            "grubbs": grubbs_test(series, alpha=grubbs_alpha),
        }
        xs = list(range(len(series)))
        coeffs = poly_fit(xs, np.nan_to_num(series), degree=trend_degree)
        mines[c]["trend_coeffs"] = coeffs
        mines[c]["trend_values"] = poly_predict(coeffs, xs)

    total_stats = series_stats(total_series)
    total_obj = {
        "stats": total_stats,
        "iqr": anomalies_iqr(total_series, k=iqr_k),
        "z": anomalies_zscore(total_series, thresh=z_thresh),
        "ma_pct": anomalies_ma_pct(total_series, window=ma_window, pct=ma_pct),
        "grubbs": grubbs_test(total_series, alpha=grubbs_alpha),
        "trend_coeffs": poly_fit(list(range(len(total_series))), total_series, trend_degree),
        "trend_values": poly_predict(poly_fit(list(range(len(total_series))), total_series, trend_degree),
                                      list(range(len(total_series))))
    }

    return {"dates": dates, "mines": mines, "total": total_obj}

# ------------------- API: /report -------------------
@app.post("/api/report")
async def make_report(payload: dict):
    analysis = payload.get("analysis")
    charts = payload.get("charts", {})

    if not analysis:
        raise HTTPException(status_code=400, detail="Analysis data missing")

    tpl = open("report_template.html").read()
    html = Template(tpl).render(analysis=analysis, charts=charts)

    
    browser = await pyppeteer.launch(
        executablePath="/usr/bin/google-chrome-stable",  
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = await browser.newPage()
    await page.setContent(html, waitUntil="networkidle0")
    pdf = await page.pdf(format="A4", printBackground=True)
    await browser.close()
    return Response(content=pdf, media_type="application/pdf")
