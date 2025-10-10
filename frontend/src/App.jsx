import React, { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const companyOptions = {
  India: ["TCS","Reliance","Adani","HDFC"],
  Japan: ["Toyota","Honda", "Sony", "Nintendo"],
  China: ["Alibaba","Xiaomi","JD.com Inc","Tencent"],
};

function App() {
  const [country, setCountry] = useState("");
  const [company, setCompany] = useState("");
  const [days, setDays] = useState(5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!company) {
      alert("Please select a company!");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/predict", {
        company,
        days
      });
      setResult(res.data);
    } catch (err) {
  if (err.response) {
    console.error("Backend returned error:", err.response.data);
    alert("Error: " + err.response.data.error);
  } else {
    console.error("Prediction error:", err);
    alert("Unexpected error while predicting");
  }
}

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Times New Roman" }}>
      <h2> Stock Forecast Dashboard</h2>

      <div>
        <label> Select Country: </label>
        <select value={country} onChange={(e) => { setCountry(e.target.value); setCompany(""); }}>
          <option value="">-- Select --</option>
          {Object.keys(companyOptions).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {country && (
        <div style={{ marginTop: "15px" }}>
          <label> Select Company: </label>
          <select value={company} onChange={(e) => setCompany(e.target.value)}>
            <option value="">-- Select --</option>
            {companyOptions[country].map((comp) => (
              <option key={comp} value={comp}>{comp}</option>
            ))}
          </select>
        </div>
      )}

      <div style={{ marginTop: "15px" }}>
        <label> Days to Forecast: </label>
        <input type="number" value={days} min="1" max="101" onChange={(e) => setDays(e.target.value)} />
      </div>

      <button onClick={handlePredict} style={{ marginTop: "20px", padding: "10px 20px" }}>
        {loading ? "Predicting..." : "Predict"}
      </button>

    {result && (
  <div style={{ marginTop: "30px" }}>
    <h3>Results for {result.company}</h3>
    <p>Low Likely: <b>{result.low_likely.toFixed(2)}</b></p>
    <p>High Likely: <b>{result.high_likely.toFixed(2)}</b></p>

    {/* Forecast Chart */}
    <div style={{ width: "600px", height: "300px", marginTop: "20px" }}>
      <Line
        data={{
          labels: Array.from({ length: result.forecast.length }, (_, i) => `Day ${i + 1}`),
          datasets: [
            {
              label: "Forecast Price",
              data: result.forecast,
              borderColor: "red",
              backgroundColor: "yellow",
              tension: 0.3,
            },
          ],
        }}
        options={{
          responsive: true,
          plugins: { legend: { display: true, position: "top" } },
        }}
      />
    </div>

    {/* Actual vs Predicted Plot */}
    {result.plot_url && (
      <div style={{ marginTop: "30px", textAlign: "center" }}>
        <h4>Actual vs Predicted Stock Prices</h4>
        <img
          src={result.plot_url}
          alt="Actual vs Predicted Plot"
          style={{
            width: "80%",
            maxWidth: "700px",
            borderRadius: "12px",
            marginTop: "10px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.15)",
          }}
        />
        <div style={{ marginTop: "10px" }}>
          <a
  href={result.plot_url}
  download={`${result.company}_plot.png`}
  style={{
    display: "inline-block",
    marginTop: "10px",
    padding: "8px 16px",
    background: "#ff00d9ff",
    color: "brown",
    borderRadius: "6px",
    textDecoration: "none",
    fontWeight: "bold",
  }}
>
  📊 Download Plot
</a>

        </div>
      </div>
    )}
  </div>
  )}
    </div>
  );
}

export default App;
