import React, { useState, useEffect, useRef } from "react";
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
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const companyOptions = {
  India: ["TCS", "Reliance", "Adani", "HDFC"],
  Japan: ["Toyota", "Honda", "Sony", "Nintendo"],
  China: ["Alibaba", "Xiaomi", "JD.com Inc", "Tencent"],
};

const countryFlags = { India: "🇮🇳", Japan: "🇯🇵", China: "🇨🇳" };
const countryColors = {
  India: { from: "#f97316", to: "#ef4444" },
  Japan: { from: "#ec4899", to: "#a855f7" },
  China: { from: "#ef4444", to: "#f59e0b" },
};

function RiskGauge({ value }) {
  const angle = (value / 100) * 180 - 90;
  const color = value < 30 ? "#22c55e" : value < 70 ? "#f59e0b" : "#ef4444";
  const label = value < 30 ? "LOW RISK" : value < 70 ? "MODERATE" : "HIGH RISK";

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px" }}>
      <svg viewBox="0 0 200 110" width="200" height="110">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22c55e" stopOpacity="0.8" />
            <stop offset="50%" stopColor="#f59e0b" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#ef4444" stopOpacity="0.8" />
          </linearGradient>
        </defs>
        {/* Track */}
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="14" strokeLinecap="round" />
        {/* Colored arc */}
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#gaugeGrad)" strokeWidth="14" strokeLinecap="round" />
        {/* Needle */}
        <g transform={`rotate(${angle}, 100, 100)`}>
          <line x1="100" y1="100" x2="100" y2="30" stroke={color} strokeWidth="3" strokeLinecap="round" />
          <circle cx="100" cy="100" r="6" fill={color} />
        </g>
        {/* Center dot */}
        <circle cx="100" cy="100" r="3" fill="white" />
      </svg>
      <div style={{ fontSize: "32px", fontWeight: "900", color, fontFamily: "'DM Mono', monospace", letterSpacing: "-1px" }}>
        {value.toFixed(1)}
      </div>
      <div style={{
        fontSize: "11px", fontWeight: "700", letterSpacing: "3px",
        color, padding: "4px 12px", borderRadius: "20px",
        border: `1px solid ${color}`, background: `${color}18`
      }}>
        {label}
      </div>
    </div>
  );
}

function StatCard({ label, value, accent }) {
  return (
    <div style={{
      flex: 1, padding: "20px 24px", borderRadius: "16px",
      background: "rgba(255,255,255,0.04)",
      border: "1px solid rgba(255,255,255,0.08)",
      backdropFilter: "blur(10px)",
      position: "relative", overflow: "hidden"
    }}>
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: "3px",
        background: `linear-gradient(90deg, ${accent}, transparent)`
      }} />
      <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "2.5px", color: "rgba(255,255,255,0.4)", marginBottom: "10px", textTransform: "uppercase" }}>
        {label}
      </div>
      <div style={{ fontSize: "28px", fontWeight: "800", color: "white", fontFamily: "'DM Mono', monospace", letterSpacing: "-1px" }}>
        {value}
      </div>
    </div>
  );
}

function PulsingDot({ color }) {
  return (
    <span style={{ position: "relative", display: "inline-flex", alignItems: "center", justifyContent: "center", width: "12px", height: "12px" }}>
      <span style={{
        position: "absolute", width: "100%", height: "100%",
        borderRadius: "50%", background: color, opacity: 0.4,
        animation: "ping 1.5s cubic-bezier(0,0,0.2,1) infinite"
      }} />
      <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: color }} />
    </span>
  );
}

export default function App() {
  const [country, setCountry] = useState("");
  const [company, setCompany] = useState("");
  const [days, setDays] = useState(5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [grsi, setGrsi] = useState(null);
  const [loadingGRSI, setLoadingGRSI] = useState(false);
  const [activeTab, setActiveTab] = useState("forecast");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Inject Google Fonts + keyframes
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap";
    document.head.appendChild(link);

    const style = document.createElement("style");
    style.innerHTML = `
      @keyframes ping { 75%,100%{transform:scale(2);opacity:0} }
      @keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
      @keyframes fadeIn { from{opacity:0} to{opacity:1} }
      @keyframes shimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }
      * { box-sizing: border-box; }
      ::-webkit-scrollbar { width: 6px; }
      ::-webkit-scrollbar-track { background: #0a0a0f; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
      select option { background: #131320; color: white; }
    `;
    document.head.appendChild(style);
  }, []);

  const accentFrom = country ? countryColors[country]?.from : "#818cf8";
  const accentTo = country ? countryColors[country]?.to : "#6366f1";

  const handlePredict = async () => {
    if (!company) return alert("Please select a company!");
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/predict", { company, days });
      setResult(res.data);
      setActiveTab("forecast");
    } catch (err) {
      alert(err?.response?.data?.error || "Unexpected error occurred");
    }
    setLoading(false);
  };

  const fetchGRSI = async () => {
    if (!company) return alert("Please select a company first!");
    setLoadingGRSI(true);
    try {
      const res = await axios.get(`http://127.0.0.1:5000/grsi?company=${company}`);
      setGrsi(res.data);
      setActiveTab("georisk");
    } catch (error) {
      alert("Failed to fetch GeoRisk Signal Index");
    }
    setLoadingGRSI(false);
  };

  const chartData = result ? {
    labels: result.forecast.map((_, i) => `D${i + 1}`),
    datasets: [{
      label: "Forecast Price",
      data: result.forecast,
      borderColor: accentFrom,
      backgroundColor: `${accentFrom}18`,
      pointBackgroundColor: accentFrom,
      pointBorderColor: "rgba(0,0,0,0.5)",
      pointRadius: result.forecast.length > 20 ? 3 : 5,
      pointHoverRadius: 7,
      borderWidth: 2.5,
      tension: 0.4,
      fill: true,
    }],
  } : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "rgba(10,10,20,0.95)",
        borderColor: "rgba(255,255,255,0.1)",
        borderWidth: 1,
        titleColor: "rgba(255,255,255,0.5)",
        bodyColor: "white",
        bodyFont: { family: "'DM Mono', monospace", weight: "bold", size: 14 },
        padding: 12,
        callbacks: {
          label: (ctx) => ` ₹ ${ctx.raw.toFixed(2)}`,
        }
      }
    },
    scales: {
      x: {
        grid: { color: "rgba(255,255,255,0.04)", drawBorder: false },
        ticks: { color: "rgba(255,255,255,0.3)", font: { family: "'DM Mono', monospace", size: 11 } },
        border: { display: false }
      },
      y: {
        grid: { color: "rgba(255,255,255,0.04)", drawBorder: false },
        ticks: { color: "rgba(255,255,255,0.3)", font: { family: "'DM Mono', monospace", size: 11 } },
        border: { display: false }
      }
    }
  };

  return (
    <div style={{
      minHeight: "100vh", background: "#07070f",
      fontFamily: "'Syne', sans-serif",
      color: "white",
      opacity: mounted ? 1 : 0,
      transition: "opacity 0.5s ease",
    }}>
      {/* Ambient background blobs */}
      <div style={{ position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0, overflow: "hidden" }}>
        <div style={{
          position: "absolute", width: "600px", height: "600px",
          borderRadius: "50%", top: "-200px", left: "-100px",
          background: `radial-gradient(circle, ${accentFrom}15 0%, transparent 70%)`,
          transition: "background 0.8s ease"
        }} />
        <div style={{
          position: "absolute", width: "500px", height: "500px",
          borderRadius: "50%", bottom: "-100px", right: "-100px",
          background: `radial-gradient(circle, ${accentTo}12 0%, transparent 70%)`,
          transition: "background 0.8s ease"
        }} />
        {/* Subtle grid */}
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: "linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px)",
          backgroundSize: "60px 60px"
        }} />
      </div>

      <div style={{ position: "relative", zIndex: 1, maxWidth: "900px", margin: "0 auto", padding: "40px 24px 80px" }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "52px", animation: "slideUp 0.6s ease both" }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: "8px",
            padding: "6px 16px", borderRadius: "30px",
            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)",
            fontSize: "12px", fontWeight: "600", letterSpacing: "2px",
            color: "rgba(255,255,255,0.5)", marginBottom: "20px"
          }}>
            <PulsingDot color="#22c55e" />
            LIVE MARKET INTELLIGENCE
          </div>
          <h1 style={{
            fontSize: "clamp(32px, 6vw, 52px)", fontWeight: "800",
            margin: 0, lineHeight: 1.1, letterSpacing: "-2px",
            background: `linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.5) 100%)`,
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            Stock Forecast
          </h1>
          <h1 style={{
            fontSize: "clamp(32px, 6vw, 52px)", fontWeight: "800",
            margin: "0 0 16px",letterSpacing: "-2px", lineHeight: 1.1,
            background: `linear-gradient(135deg, ${accentFrom}, ${accentTo})`,
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            transition: "background 0.5s ease"
          }}>
            + GeoRisk Index
          </h1>
          <p style={{ color: "rgba(255,255,255,0.35)", fontSize: "15px", margin: 0, fontWeight: "500" }}>
            ML-powered predictions with geopolitical risk analysis
          </p>
        </div>

        {/* Control Panel */}
        <div style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.08)",
          borderRadius: "24px",
          padding: "32px",
          backdropFilter: "blur(20px)",
          marginBottom: "28px",
          animation: "slideUp 0.6s 0.1s ease both"
        }}>
          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", alignItems: "flex-end" }}>

            {/* Country */}
            <div style={{ flex: "1 1 160px" }}>
              <label style={labelStyle}>Market Region</label>
              <div style={{ position: "relative" }}>
                <select
                  style={selectStyle(accentFrom)}
                  value={country}
                  onChange={(e) => { setCountry(e.target.value); setCompany(""); setGrsi(null); setResult(null); }}
                >
                  <option value="">— Select —</option>
                  {Object.keys(companyOptions).map((c) => (
                    <option key={c} value={c}>{countryFlags[c]} {c}</option>
                  ))}
                </select>
                <span style={{ position: "absolute", right: "14px", top: "50%", transform: "translateY(-50%)", pointerEvents: "none", fontSize: "12px", color: "rgba(255,255,255,0.4)" }}>▾</span>
              </div>
            </div>

            {/* Company */}
            <div style={{ flex: "1 1 180px" }}>
              <label style={labelStyle}>Company</label>
              <div style={{ position: "relative" }}>
                <select
                  style={selectStyle(accentFrom)}
                  value={company}
                  onChange={(e) => { setCompany(e.target.value); setGrsi(null); }}
                  disabled={!country}
                >
                  <option value="">— Select —</option>
                  {(companyOptions[country] || []).map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                <span style={{ position: "absolute", right: "14px", top: "50%", transform: "translateY(-50%)", pointerEvents: "none", fontSize: "12px", color: "rgba(255,255,255,0.4)" }}>▾</span>
              </div>
            </div>

            {/* Days */}
            <div style={{ flex: "0 1 130px" }}>
              <label style={labelStyle}>Forecast Days</label>
              <input
                type="number" min="1" max="101" value={days}
                style={selectStyle(accentFrom)}
                onChange={(e) => setDays(e.target.value)}
              />
            </div>

            {/* Buttons */}
            <div style={{ flex: "1 1 200px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
              <button
                onClick={handlePredict}
                disabled={loading || !company}
                style={{
                  flex: 1, padding: "14px 20px",
                  background: loading || !company ? "rgba(255,255,255,0.05)" : `linear-gradient(135deg, ${accentFrom}, ${accentTo})`,
                  color: loading || !company ? "rgba(255,255,255,0.3)" : "white",
                  border: "none", borderRadius: "12px",
                  fontWeight: "700", fontSize: "14px",
                  cursor: loading || !company ? "not-allowed" : "pointer",
                  fontFamily: "'Syne', sans-serif",
                  letterSpacing: "0.5px",
                  transition: "all 0.3s ease",
                  position: "relative", overflow: "hidden",
                  whiteSpace: "nowrap",
                }}
              >
                {loading ? (
                  <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
                    <span style={{
                      width: "14px", height: "14px", borderRadius: "50%",
                      border: "2px solid rgba(255,255,255,0.3)",
                      borderTopColor: "white",
                      animation: "spin 0.8s linear infinite",
                      display: "inline-block"
                    }} />
                    Predicting...
                  </span>
                ) : "⚡ Predict"}
              </button>
              <button
                onClick={fetchGRSI}
                disabled={loadingGRSI || !company}
                style={{
                  flex: 1, padding: "14px 20px",
                  background: loadingGRSI || !company ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.07)",
                  color: loadingGRSI || !company ? "rgba(255,255,255,0.3)" : "white",
                  border: `1px solid ${loadingGRSI || !company ? "rgba(255,255,255,0.06)" : "rgba(255,255,255,0.15)"}`,
                  borderRadius: "12px",
                  fontWeight: "700", fontSize: "14px",
                  cursor: loadingGRSI || !company ? "not-allowed" : "pointer",
                  fontFamily: "'Syne', sans-serif",
                  transition: "all 0.3s ease",
                  whiteSpace: "nowrap",
                }}
              >
                {loadingGRSI ? "Loading..." : "🌐 GeoRisk"}
              </button>
            </div>
          </div>
        </div>

        {/* Company Badge */}
        {company && (
          <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "28px", animation: "fadeIn 0.4s ease both" }}>
            <div style={{
              display: "flex", alignItems: "center", gap: "10px",
              padding: "8px 16px 8px 10px",
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: "40px"
            }}>
              <span style={{ fontSize: "22px" }}>{countryFlags[country]}</span>
              <span style={{ fontWeight: "700", fontSize: "15px" }}>{company}</span>
              <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.35)", fontWeight: "600", letterSpacing: "1px" }}>· {country.toUpperCase()}</span>
            </div>
          </div>
        )}

        {/* Tabs */}
        {(result || grsi) && (
          <div style={{ display: "flex", gap: "4px", marginBottom: "24px", padding: "4px", background: "rgba(255,255,255,0.04)", borderRadius: "14px", width: "fit-content" }}>
            {result && (
              <button onClick={() => setActiveTab("forecast")} style={tabStyle(activeTab === "forecast", accentFrom)}>
                📈 Forecast
              </button>
            )}
            {grsi?.GRSI && (
              <button onClick={() => setActiveTab("georisk")} style={tabStyle(activeTab === "georisk", accentFrom)}>
                🌐 GeoRisk
              </button>
            )}
            {result?.plot_url && (
              <button onClick={() => setActiveTab("chart")} style={tabStyle(activeTab === "chart", accentFrom)}>
                🖼 Model Plot
              </button>
            )}
          </div>
        )}

        {/* Forecast Tab */}
        {result && activeTab === "forecast" && (
          <div style={{ animation: "slideUp 0.4s ease both" }}>
            {/* Stat Cards */}
            <div style={{ display: "flex", gap: "16px", marginBottom: "24px", flexWrap: "wrap" }}>
              <StatCard label="Low Likely" value={`${result.low_likely.toFixed(2)}`} accent="#22c55e" />
              <StatCard label="High Likely" value={`${result.high_likely.toFixed(2)}`} accent={accentFrom} />
              <StatCard label="Forecast Horizon" value={`${result.forecast.length}d`} accent={accentTo} />
            </div>

            {/* Chart */}
            <div style={{
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.07)",
              borderRadius: "24px", padding: "28px",
              backdropFilter: "blur(20px)"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
                <div>
                  <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "2px", color: "rgba(255,255,255,0.35)", marginBottom: "4px" }}>PRICE FORECAST</div>
                  <div style={{ fontWeight: "800", fontSize: "18px" }}>{result.company}</div>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px", color: "rgba(255,255,255,0.4)" }}>
                  <span style={{ width: "20px", height: "2px", background: `linear-gradient(90deg, ${accentFrom}, ${accentTo})`, display: "inline-block", borderRadius: "2px" }} />
                  Predicted
                </div>
              </div>
              <div style={{ height: "300px" }}>
                <Line data={chartData} options={chartOptions} />
              </div>
            </div>
          </div>
        )}

        {/* GeoRisk Tab */}
        {grsi?.GRSI && activeTab === "georisk" && (
          <div style={{
            animation: "slideUp 0.4s ease both",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "24px", padding: "40px 32px",
            backdropFilter: "blur(20px)",
            display: "flex", flexDirection: "column", alignItems: "center", gap: "20px"
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "2px", color: "rgba(255,255,255,0.35)", marginBottom: "6px" }}>GEORISK SIGNAL INDEX</div>
              <div style={{ fontWeight: "800", fontSize: "22px" }}>{grsi.company}</div>
            </div>
            <RiskGauge value={grsi.GRSI} />
            <p style={{ color: "rgba(255,255,255,0.35)", fontSize: "13px", textAlign: "center", maxWidth: "360px", lineHeight: 1.6, margin: 0 }}>
              Higher score indicates greater geopolitical tension and potential market volatility.
            </p>
            {/* Mini risk scale */}
            <div style={{ display: "flex", gap: "10px", marginTop: "4px" }}>
              {[["LOW", "#22c55e", "0–30"], ["MODERATE", "#f59e0b", "30–70"], ["HIGH", "#ef4444", "70–100"]].map(([lbl, color, range]) => (
                <div key={lbl} style={{
                  padding: "8px 16px", borderRadius: "10px",
                  background: `${color}12`, border: `1px solid ${color}30`,
                  textAlign: "center"
                }}>
                  <div style={{ fontSize: "10px", fontWeight: "700", color, letterSpacing: "1.5px" }}>{lbl}</div>
                  <div style={{ fontSize: "12px", color: "rgba(255,255,255,0.4)", marginTop: "2px", fontFamily: "'DM Mono', monospace" }}>{range}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Model Plot Tab */}
        {result?.plot_url && activeTab === "chart" && (
          <div style={{
            animation: "slideUp 0.4s ease both",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "24px", padding: "28px",
            backdropFilter: "blur(20px)"
          }}>
            <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "2px", color: "rgba(255,255,255,0.35)", marginBottom: "20px" }}>ACTUAL vs PREDICTED</div>
            <img src={result.plot_url} alt="Stock Plot" style={{ width: "100%", borderRadius: "16px", display: "block" }} />
            <a href={result.plot_url} download={`${result.company}_plot.png`} style={{
              display: "inline-flex", alignItems: "center", gap: "8px",
              marginTop: "20px", padding: "10px 20px",
              background: `linear-gradient(135deg, ${accentFrom}22, ${accentTo}22)`,
              border: `1px solid ${accentFrom}44`,
              color: "white", borderRadius: "10px",
              textDecoration: "none", fontWeight: "600", fontSize: "14px",
              transition: "all 0.2s ease"
            }}>
              ↓ Download Plot
            </a>
          </div>
        )}

      </div>

      {/* Spinner keyframe injection */}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

// Shared style helpers
const labelStyle = {
  display: "block",
  fontSize: "11px", fontWeight: "600",
  letterSpacing: "2px", color: "rgba(255,255,255,0.4)",
  marginBottom: "8px", textTransform: "uppercase"
};

const selectStyle = (accent) => ({
  width: "100%", padding: "13px 36px 13px 14px",
  background: "rgba(255,255,255,0.05)",
  border: "1px solid rgba(255,255,255,0.1)",
  borderRadius: "12px", color: "white",
  fontFamily: "'Syne', sans-serif",
  fontWeight: "600", fontSize: "14px",
  outline: "none", appearance: "none",
  cursor: "pointer",
  transition: "border-color 0.2s ease",
});

const tabStyle = (active, accent) => ({
  padding: "9px 18px",
  background: active ? "rgba(255,255,255,0.08)" : "transparent",
  border: active ? "1px solid rgba(255,255,255,0.12)" : "1px solid transparent",
  borderRadius: "10px", color: active ? "white" : "rgba(255,255,255,0.4)",
  fontFamily: "'Syne', sans-serif",
  fontWeight: "700", fontSize: "13px",
  cursor: "pointer", transition: "all 0.2s ease",
});