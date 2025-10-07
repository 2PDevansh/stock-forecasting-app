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
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
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
        <input type="number" value={days} min="1" max="30" onChange={(e) => setDays(e.target.value)} />
      </div>

      <button onClick={handlePredict} style={{ marginTop: "20px", padding: "10px 20px" }}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h3> Results for {result.company}</h3>
          <p> Low Likely: <b>{result.low_likely.toFixed(2)}</b></p>
          <p> High Likely: <b>{result.high_likely.toFixed(2)}</b></p>

          <div style={{ width: "600px", height: "300px", marginTop: "20px" }}>
            <Line
              data={{
                labels: Array.from({ length: result.forecast.length }, (_, i) => `Day ${i + 1}`),
                datasets: [
                  {
                    label: "Forecast Price",
                    data: result.forecast,
                    borderColor: "blue",
                    backgroundColor: "lightblue"
                  }
                ]
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
