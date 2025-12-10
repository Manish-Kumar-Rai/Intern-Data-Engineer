import React, { useState, useEffect } from "react";
import { fetchData, analyze, generateReport } from "./api";
import ChartPanel from "./components/ChartPanel";
import Controls from "./components/Controls";
import Summary from "./components/Summary";

export default function App() {
  const [raw, setRaw] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [chartType, setChartType] = useState("line"); // line, bar, stacked
  const [trendDegree, setTrendDegree] = useState(1);   // polynomial degree 1-4
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
      const charts = {}; // Optionally capture chart images from ChartPanel
      const blob = await generateReport({ analysis, charts });

      // Create a proper Blob for PDF download
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
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Mining Dashboard</h1>
      <Controls
        params={params}
        setParams={setParams}
        onAnalyze={runAnalyze}
        onExport={exportPdf}
        chartType={chartType}
        setChartType={setChartType}
        trendDegree={trendDegree}
        setTrendDegree={setTrendDegree}
        loadingAnalysis={loadingAnalysis}
        loadingPdf={loadingPdf}
      />
      <Summary analysis={analysis} />
      <ChartPanel analysis={analysis} chartType={chartType} trendDegree={trendDegree} />
    </div>
  );
}
