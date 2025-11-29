import React, { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const companyOptions = {
  India: ["TCS", "Reliance", "Adani", "HDFC"],
  Japan: ["Toyota", "Honda", "Sony", "Nintendo"],
  China: ["Alibaba", "Xiaomi", "JD.com Inc", "Tencent"],
};

function App() {
  const [country, setCountry] = useState("");
  const [company, setCompany] = useState("");
  const [days, setDays] = useState(5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [grsi, setGrsi] = useState(null);
  const [loadingGRSI, setLoadingGRSI] = useState(false);

  // ---------- STOCK PREDICTION ----------
  const handlePredict = async () => {
    if (!company) return alert("Please select a company!");

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/predict", { company, days });
      setResult(res.data);
    } catch (err) {
      console.error("Prediction error:", err?.response?.data || err);
      alert(err?.response?.data?.error || "Unexpected error occurred");
    }
    setLoading(false);
  };

  // ---------- GRSI FETCH ----------
  const fetchGRSI = async () => {
    if (!company) return alert("Please select a company first!");

    setLoadingGRSI(true);
    try {
      const res = await axios.get(`http://127.0.0.1:5000/grsi?company=${company}`);
      setGrsi(res.data);
    } catch (error) {
      console.error("GRSI Fetch Error:", error);
      alert("Failed to fetch GeoRisk Signal Index");
    }
    setLoadingGRSI(false);
  };

  // ---------- RISK BADGE COLOR ----------
  const getRiskColor = (value) => {
    if (value < 30) return "green";
    if (value < 70) return "orange";
    return "red";
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Stock Forecast Dashboard + GeoRisk Index</h2>

      {/* Country Dropdown */}
      <div style={styles.inputGroup}>
        <label style={styles.label}>Select Country:</label>
        <select
          style={styles.select}
          value={country}
          onChange={(e) => { setCountry(e.target.value); setCompany(""); setGrsi(null); }}
        >
          <option value="">-- Select --</option>
          {Object.keys(companyOptions).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {/* Company Dropdown */}
      {country && (
        <div style={styles.inputGroup}>
          <label style={styles.label}>Select Company:</label>
          <select
            style={styles.select}
            value={company}
            onChange={(e) => { setCompany(e.target.value); setGrsi(null); }}
          >
            <option value="">-- Select --</option>
            {companyOptions[country].map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      )}

      {/* Days Input */}
      <div style={styles.inputGroup}>
        <label style={styles.label}>Days to Forecast:</label>
        <input
          type="number"
          min="1"
          max="101"
          value={days}
          style={styles.input}
          onChange={(e) => setDays(e.target.value)}
        />
      </div>

      {/* Predict Button */}
      <button style={styles.button} onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {/* GRSI Button */}
      <button style={styles.buttonSecondary} onClick={fetchGRSI} disabled={loadingGRSI}>
        {loadingGRSI ? "Loading GRSI..." : "Show GeoRisk Index"}
      </button>

      {/* Forecast Results */}
      {result && (
        <div style={styles.resultBox}>
          <h3>Results for <b>{result.company}</b></h3>
          <p>Low Likely: <b>{result.low_likely.toFixed(2)}</b></p>
          <p>High Likely: <b>{result.high_likely.toFixed(2)}</b></p>

          <div style={styles.chartContainer}>
            <Line
              data={{
                labels: result.forecast.map((_, i) => `Day ${i + 1}`),
                datasets: [
                  {
                    label: "Forecast Price",
                    data: result.forecast,
                    borderColor: "rgba(255, 99, 132, 1)",
                    backgroundColor: "rgba(255, 99, 132, 0.3)",
                    tension: 0.35,
                  }
                ],
              }}
              options={{ responsive: true }}
            />
          </div>

          {result.plot_url && (
            <>
              <h4>Actual vs Predicted Stock Prices</h4>
              <img src={result.plot_url} alt="Stock Plot" style={styles.image} />
              <a href={result.plot_url} download={`${result.company}_plot.png`} style={styles.downloadBtn}>
                Download Plot
              </a>
            </>
          )}
        </div>
      )}

      {/* GRSI Display */}
      {grsi?.GRSI && (
        <div style={styles.grsiBox}>
          <h3>GeoRisk Score for <b>{grsi.company}</b></h3>

          <p style={{
            fontSize: "28px",
            fontWeight: "700",
            color: getRiskColor(grsi.GRSI)
          }}>
            {grsi.GRSI.toFixed(2)}
          </p>

          <p style={{ fontSize: "14px" }}>
            Higher score → Higher geopolitical tension & market volatility.
          </p>
        </div>
      )}
    </div>
  );
}

// ---------- STYLES ----------
const styles = {
  container: { padding: "25px", fontFamily: "Inter, sans-serif", textAlign: "center" },
  header: { color: "#2E4057", fontWeight: "700" },
  inputGroup: { marginTop: "15px" },
  label: { fontWeight: "600", marginRight: "10px" },
  select: { padding: "6px 10px", borderRadius: "6px" },
  input: { width: "90px", padding: "6px", borderRadius: "6px" },
  button: {
    marginTop: "25px", padding: "10px 25px", background: "#2E4057",
    color: "white", borderRadius: "8px", cursor: "pointer",
  },
  buttonSecondary: {
    marginTop: "15px", padding: "10px 25px", background: "#B73E3E",
    color: "white", borderRadius: "8px", cursor: "pointer"
  },
  resultBox: { marginTop: "30px", padding: "20px" },
  chartContainer: { width: "650px", height: "350px", margin: "20px auto" },
  grsiBox: {
    marginTop: "30px",
    padding: "20px",
    background: "#fafafa",
    borderRadius: "10px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
  },
  image: { width: "80%", maxWidth: "700px", borderRadius: "12px", marginTop: "20px" },
  downloadBtn: {
    display: "inline-block", marginTop: "15px", padding: "8px 16px",
    background: "#E8D9B5", color: "#532E1C", borderRadius: "6px", textDecoration: "none"
  }
};

export default App;
