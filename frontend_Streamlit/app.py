import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Forecast + GeoRisk Index", layout="wide")

# -------------------- UI CONFIG --------------------
st.title("Stock Forecast Dashboard + GeoRisk Signal Index")

company_options = {
    "India": ["TCS", "Reliance", "Adani", "HDFC"],
    "Japan": ["Toyota", "Honda", "Sony", "Nintendo"],
    "China": ["Alibaba", "Xiaomi", "JD.com Inc", "Tencent"],
}

BACKEND_URL = "http://127.0.0.1:5000"

# -------------------- DROPDOWNS --------------------
country = st.selectbox("Select Country", [""] + list(company_options.keys()))
company = None
if country:
    company = st.selectbox("Select Company", [""] + company_options[country])

days = st.number_input("Days to Forecast", min_value=1, max_value=101, value=5)

# -------------------- ACTION BUTTONS --------------------
col1, col2 = st.columns(2)

with col1:
    predict_btn = st.button("Predict Stock Price", use_container_width=True)

with col2:
    grsi_btn = st.button("Show GeoRisk Index", use_container_width=True)


# -------------------- FORECAST REQUEST --------------------
if predict_btn:
    if not company:
        st.error("Select a company to predict!")
    else:
        with st.spinner("Predicting... Please wait "):
            try:
                res = requests.post(f"{BACKEND_URL}/predict",
                                    json={"company": company, "days": days})
                result = res.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.subheader(f"Results for **{result['company']}**")
                    st.write(f"Low Likely: **{result['low_likely']:.2f}**")
                    st.write(f"High Likely: **{result['high_likely']:.2f}**")

                    # ----------- Plot Forecast Data ----------
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        y=result["forecast"],
                        mode="lines+markers",
                        name="Forecast Price"
                    ))
                    fig.update_layout(
                        title="Forecasted Stock Prices",
                        xaxis_title="Days",
                        yaxis_title="Price",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Saved matplotlib plot
                    if result.get("plot_url"):
                        st.subheader("Actual vs Predicted Stock Prices")
                        st.image(result["plot_url"])
                        st.download_button(
                            "Download Plot",
                            data=requests.get(result["plot_url"]).content,
                            file_name=f"{company}_plot.png",
                            mime="image/png"
                        )

            except Exception as e:
                st.error(f"Prediction Error: {e}")


# -------------------- GRSI FETCH --------------------
if grsi_btn:
    if not company:
        st.error("Please select a company first!")
    else:
        with st.spinner("Fetching GeoRisk Score..."):
            try:
                response = requests.get(f"{BACKEND_URL}/grsi?company={company}").json()

                # Ensure valid key returned
                if "GRSI" not in response:
                    st.error("No GRSI value returned from server")
                else:
                    score = response["GRSI"]

                    st.subheader(f"GeoRisk Score for **{response['company']}**")

                    if score < 30:
                        risk_label = "🟢 Low Risk"
                    elif score < 70:
                        risk_label = "🟠 Medium Risk"
                    else:
                        risk_label = "🔴 High Risk"

                    st.markdown(
                        f"""
                        <div style="font-size:45px; font-weight:700; text-align:center;">
                            {score:.2f}
                        </div>
                        <p style='text-align:center;font-size:18px;'>{risk_label}</p>
                        <p style='text-align:center;font-size:14px;'>Higher score → Higher geopolitical tension & volatility.</p>
                        """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error(f"Failed to fetch GRSI data: {e}")
