import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from agents import run_agent, simulate_debate
from consensus import calculate_confidence, capital_allocation

st.set_page_config(page_title="AIC-DAO", layout="wide")

# ---------- Institutional CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0B1120;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    margin-top: 25px;
}

.hero-sub {
    font-size: 15px;
    color: #94A3B8;
    margin-bottom: 25px;
}

.meta {
    font-size: 12px;
    color: #64748B;
    letter-spacing: 0.5px;
    margin-bottom: 40px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 50px;
    margin-bottom: 20px;
}

.resolution-box {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    padding: 40px;
    border-radius: 14px;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 30px;
}

.resolution-title {
    font-size: 12px;
    color: #64748B;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.resolution-decision {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 20px;
}

.resolution-metrics {
    font-size: 18px;
    margin-bottom: 8px;
}

.transcript {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    padding: 25px;
    border-radius: 12px;
    margin-top: 20px;
}

.agent-label {
    font-weight: 600;
    margin-top: 15px;
}

.footer {
    text-align:center;
    font-size:13px;
    color:#475569;
    margin-top:60px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="hero-title">AIC-DAO</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Autonomous Capital Evaluation Infrastructure</div>', unsafe_allow_html=True)

evaluation_id = f"AIC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
timestamp = datetime.datetime.now().strftime("%d %b %Y | %H:%M")

st.markdown(
    f'<div class="meta">Evaluation ID: {evaluation_id} &nbsp;&nbsp;|&nbsp;&nbsp; Timestamp: {timestamp}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- Mode ----------
mode = st.radio(
    "Evaluation Mode",
    ["Startup", "Public Company"],
    horizontal=True
)

# ---------- Inputs ----------
st.markdown('<div class="section-title">Entity Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Entity Name", "FlowBridge")
    sector = st.text_input("Sector / Industry", "Cross-chain Liquidity Protocol")
    revenue = st.text_input("Revenue Status", "Pre-revenue")
    traction = st.text_input("Market Position / Traction", "1200 beta users")

with col2:
    raised = st.number_input("Capital Raised ($)", value=150000)
    burn = st.number_input("Monthly Burn ($)", value=20000)
    runway = st.number_input("Runway (months)", value=7)
    governance = st.text_input("Governance / Capital Structure", "Governance token")

# ---------- Execution ----------
if st.button("Run Capital Evaluation"):

    entity_data = f"""
    Name: {name}
    Sector: {sector}
    Raised: {raised}
    Burn: {burn}
    Runway: {runway}
    Traction: {traction}
    Revenue: {revenue}
    Governance: {governance}
    Mode: {mode}
    """

    with st.spinner("Coordinating multi-agent capital review..."):
        time.sleep(0.5)

        risk = run_agent("Risk Analyst", entity_data)
        market = run_agent("Market Analyst", entity_data)
        capital = run_agent("Capital Structure Analyst", entity_data)

        confidence = calculate_confidence(
            risk["score"], market["score"], capital["score"]
        )

        allocation = capital_allocation(confidence)
        debate = simulate_debate(risk, market)

    # ---------- Resolution Block ----------
    st.markdown('<div class="resolution-box">', unsafe_allow_html=True)
    st.markdown('<div class="resolution-title">CAPITAL COMMITTEE RESOLUTION</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="resolution-decision">{allocation["decision"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="resolution-metrics">Recommended Allocation: ${allocation["allocation"]:,}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="resolution-metrics">Downside Risk Probability: {allocation["risk_probability"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Confidence Gauge ----------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range':[0,1]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------- Structured Transcript ----------
    st.markdown('<div class="section-title">Structured Agent Exchange</div>', unsafe_allow_html=True)
    st.markdown('<div class="transcript">', unsafe_allow_html=True)

    st.markdown('<div class="agent-label">Risk Analyst</div>', unsafe_allow_html=True)
    st.write(risk["analysis"])

    st.markdown('<div class="agent-label">Market Analyst</div>', unsafe_allow_html=True)
    st.write(market["analysis"])

    st.markdown('<div class="agent-label">Deliberation Outcome</div>', unsafe_allow_html=True)
    st.write(debate)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown('<div class="footer">AIC-DAO • Institutional Autonomous Capital Infrastructure • v4.0</div>', unsafe_allow_html=True)
