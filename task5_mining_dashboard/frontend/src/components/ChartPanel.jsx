import React from "react";
import { Line, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

export default function ChartPanel({ analysis, chartType }) {
  if (!analysis) return null;

  const labels = analysis.dates;

  const datasets = Object.entries(analysis.mines).map(([mine, data]) => {
    const series = data.trend_values;
    const anomalies = [...data.iqr, ...data.z, ...data.ma_pct, ...data.grubbs];
    const anomalyIndices = anomalies.map(a => a.i);

    return {
      label: mine,
      data: series,
      borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`,
      backgroundColor: `hsla(${Math.random() * 360}, 70%, 50%, 0.3)`,
      pointRadius: series.map((_, idx) => (anomalyIndices.includes(idx) ? 6 : 3)),
      pointBackgroundColor: series.map((_, idx) => (anomalyIndices.includes(idx) ? "red" : "blue")),
    };
  });

  const data = {
    labels,
    datasets,
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Mine Outputs with Trendline & Anomalies" },
    },
    scales: {
      y: { beginAtZero: false },
      x: { beginAtZero: true },
    },
  };

  if (chartType === "line") return <Line data={data} options={options} />;
  if (chartType === "bar") return <Bar data={data} options={options} />;
  if (chartType === "stacked") {
    return <Bar data={{ ...data, datasets: datasets.map(ds => ({ ...ds, stack: "Stack 0" })) }} options={{ ...options, scales: { x: { stacked: true }, y: { stacked: true } } }} />;
  }

  return null;
}
