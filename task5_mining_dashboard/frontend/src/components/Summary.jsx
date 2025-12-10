import React from "react";

export default function Summary({ analysis }) {
  if (!analysis) return null;

  const renderStats = (name, stats, anomalies) => (
    <div
      key={name}
      style={{
        border: "1px solid #ccc",
        padding: "1rem",
        margin: "0.5rem",
        borderRadius: "8px",
        background: "#f9f9f9",
        minWidth: "180px",
      }}
    >
      <h3>{name}</h3>
      <p>Mean: {stats.mean.toFixed(2)}</p>
      <p>Std Dev: {stats.std.toFixed(2)}</p>
      <p>Median: {stats.median.toFixed(2)}</p>
      <p>IQR: {stats.iqr.toFixed(2)}</p>
      <p>Anomalies: {anomalies.length}</p>
    </div>
  );

  return (
    <div style={{ display: "flex", flexWrap: "wrap" }}>
      {Object.entries(analysis.mines).map(([mine, data]) =>
        renderStats(
          mine,
          data.stats,
          [...data.iqr, ...data.z, ...data.ma_pct, ...data.grubbs]
        )
      )}
      {renderStats(
        "Total",
        analysis.total.stats,
        [...analysis.total.iqr, ...analysis.total.z, ...analysis.total.ma_pct, ...analysis.total.grubbs]
      )}
    </div>
  );
}
