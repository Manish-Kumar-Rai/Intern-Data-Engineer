import React, { useState, useEffect } from "react";
import { fetchData, analyze, generateReport } from "./api";
import ChartPanel from "./components/ChartPanel";
import Controls from "./components/Controls";
import Summary from "./components/Summary";

export default function App() {
  const [raw, setRaw] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [chartType, setChartType] = useState("line");
  const [trendDegree, setTrendDegree] = useState(1);
  const [params, setParams] = useState({
    iqr_k: 1.5,
    z_thresh: 3,
    ma_window: 7,
    ma_pct: 0.3,
    grubbs_alpha: 0.05,
    trend_degree: 1
  });
  const [loadingPdf, setLoadingPdf] = useState(false);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  useEffect(() => {
    fetchData().then(setRaw).catch(err => console.error("Fetch data error:", err));
  }, []);

  const runAnalyze = async () => {
    try {
      setLoadingAnalysis(true);
      const res = await analyze({ params: { ...params, trend_degree: trendDegree } });
      setAnalysis(res);
    } catch (err) {
      console.error("Analyze error:", err);
      alert("Failed to run analysis. Check console for details.");
    } finally {
      setLoadingAnalysis(false);
    }
  };

  const exportPdf = async () => {
    if (!analysis) return alert("Run analysis first!");
    try {
      setLoadingPdf(true);
      const charts = {};
      const blob = await generateReport({ analysis, charts });
      const pdfBlob = new Blob([blob], { type: "application/pdf" });
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "Mining_Report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF generation error:", err);
      alert("Failed to generate PDF. Check console for details.");
    } finally {
      setLoadingPdf(false);
    }
  };

  return (
    <div style={{ fontFamily: "'Segoe UI', Roboto, sans-serif", backgroundColor: "#f4f6f9", minHeight: "100vh" }}>
      <header style={{ backgroundColor: "#0d47a1", color: "#fff", padding: "1rem 2rem", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h1 style={{ margin: 0, fontSize: "1.8rem" }}>Weyland-Yutani Mining Dashboard</h1>
        <button
          onClick={exportPdf}
          disabled={loadingPdf || !analysis}
          style={{
            backgroundColor: "#ffb300",
            border: "none",
            padding: "0.5rem 1rem",
            borderRadius: "4px",
            fontWeight: "bold",
            cursor: "pointer"
          }}
        >
          {loadingPdf ? "Generating PDF..." : "Export PDF"}
        </button>
      </header>

      <main style={{ display: "flex", padding: "2rem", gap: "2rem" }}>
        <aside style={{ flex: "0 0 300px", backgroundColor: "#fff", padding: "1rem", borderRadius: "8px", boxShadow: "0 2px 6px rgba(0,0,0,0.1)" }}>
          <Controls
            params={params}
            setParams={setParams}
            onAnalyze={runAnalyze}
            chartType={chartType}
            setChartType={setChartType}
            trendDegree={trendDegree}
            setTrendDegree={setTrendDegree}
            loadingAnalysis={loadingAnalysis}
          />
        </aside>

        <section style={{ flex: 1, display: "flex", flexDirection: "column", gap: "2rem" }}>
          <Summary analysis={analysis} />
          <div style={{ backgroundColor: "#fff", padding: "1rem", borderRadius: "8px", boxShadow: "0 2px 6px rgba(0,0,0,0.1)" }}>
            <ChartPanel analysis={analysis} chartType={chartType} trendDegree={trendDegree} />
          </div>
        </section>
      </main>

      <footer style={{ textAlign: "center", padding: "1rem", marginTop: "2rem", color: "#777" }}>
        &copy; {new Date().getFullYear()} Weyland-Yutani Corporation
      </footer>
    </div>
  );
}
