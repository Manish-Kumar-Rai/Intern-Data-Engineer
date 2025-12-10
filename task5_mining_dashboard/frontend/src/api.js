import axios from 'axios';
const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
export async function fetchData(){ return (await axios.get(`${API}/api/data`)).data; }
export async function analyze(params){ return (await axios.post(`${API}/api/analyze`, {params})).data; }
export async function generateReport({analysis, charts}) {
  const res = await axios.post(`${API}/api/report`, {analysis, charts}, { responseType: 'blob' });
  return res.data;
}

