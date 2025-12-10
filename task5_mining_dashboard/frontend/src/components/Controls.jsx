import React from "react";

export default function Controls({
  params,
  setParams,
  onAnalyze,
  onExport,
  chartType,
  setChartType,
  trendDegree,
  setTrendDegree,
}) {
  const handleChange = (e) => {
    setParams({ ...params, [e.target.name]: parseFloat(e.target.value) });
  };

  return (
    <div style={{ marginBottom: "1rem", display: "flex", gap: "1rem", flexWrap: "wrap" }}>
      <label>
        Chart Type:
        <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
          <option value="line">Line</option>
          <option value="bar">Bar</option>
          <option value="stacked">Stacked</option>
        </select>
      </label>

      <label>
        Trend Degree:
        <select value={trendDegree} onChange={(e) => setTrendDegree(parseInt(e.target.value))}>
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
        </select>
      </label>

      <label>
        IQR k:
        <input type="number" step="0.1" name="iqr_k" value={params.iqr_k} onChange={handleChange} />
      </label>

      <label>
        Z-thresh:
        <input type="number" step="0.1" name="z_thresh" value={params.z_thresh} onChange={handleChange} />
      </label>

      <label>
        MA window:
        <input type="number" name="ma_window" value={params.ma_window} onChange={handleChange} />
      </label>

      <label>
        MA pct:
        <input type="number" step="0.01" name="ma_pct" value={params.ma_pct} onChange={handleChange} />
      </label>

      <label>
        Grubbs alpha:
        <input type="number" step="0.01" name="grubbs_alpha" value={params.grubbs_alpha} onChange={handleChange} />
      </label>

      <button onClick={onAnalyze}>Run Analysis</button>
      <button onClick={onExport}>Export PDF</button>
    </div>
  );
}
