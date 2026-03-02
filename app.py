import streamlit as st
import plotly.graph_objects as go
import time
from agents import run_agent, simulate_debate
from consensus import calculate_confidence, capital_allocation

st.set_page_config(page_title="AIC-DAO", layout="wide")

# ---------- Clean Minimal CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0F172A;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 40px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-top: 30px;
}

.hero-sub {
    font-size: 16px;
    color: #94A3B8;
    margin-bottom: 40px;
}

.card {
    background-color: #111827;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #1F2937;
    margin-bottom: 20px;
}

.metric-label {
    font-size: 14px;
    color: #9CA3AF;
}

.metric-value {
    font-size: 26px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="hero-title">AIC-DAO</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Autonomous Capital Evaluation Infrastructure</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- Mode Selector ----------
mode = st.radio(
    "Evaluation Mode",
    ["Startup", "Public Company"],
    horizontal=True
)

# ---------- Input Section ----------
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

st.markdown("")

# ---------- Execution ----------
if st.button("Run Capital Evaluation"):

    if mode == "Startup":
        entity_data = f"""
        Name: {name}
        Sector: {sector}
        Raised: {raised}
        Burn: {burn}
        Runway: {runway}
        Traction: {traction}
        Revenue: {revenue}
        Governance: {governance}
        Entity Type: Early-Stage Venture
        """
    else:
        entity_data = f"""
        Company: {name}
        Industry: {sector}
        Market Position: {traction}
        Revenue Status: {revenue}
        Capital Structure: {governance}
        Regulatory Exposure: Moderate
        Entity Type: Public Corporation
        """

    with st.spinner("Coordinating multi-agent analysis..."):
        time.sleep(0.4)

        if mode == "Startup":
            risk = run_agent("Early-Stage Risk Analyst", entity_data)
            market = run_agent("Startup Market & Moat Analyst", entity_data)
            capital = run_agent("Tokenomics & Governance Analyst", entity_data)
        else:
            risk = run_agent("Regulatory & Macro Risk Analyst", entity_data)
            market = run_agent("Competitive Moat & Market Share Analyst", entity_data)
            capital = run_agent("Capital Efficiency & Governance Analyst", entity_data)

        confidence = calculate_confidence(
            risk["score"], market["score"], capital["score"]
        )

        allocation = capital_allocation(confidence)
        debate = simulate_debate(risk, market)

    # ---------- Output Section ----------
    st.markdown('<div class="section-title">Consensus Output</div>', unsafe_allow_html=True)

    # Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range':[0,1]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Radar
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[risk["score"], market["score"], capital["score"], risk["score"]],
        theta=["Risk","Market","Capital","Risk"],
        fill='toself'
    ))
    radar.update_layout(polar=dict(radialaxis=dict(range=[0,1])), showlegend=False)

    st.plotly_chart(radar, use_container_width=True)

    # Allocation Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Decision</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{allocation["decision"]}</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('<div class="metric-label">Recommended Allocation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">${allocation["allocation"]:,}</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('<div class="metric-label">Downside Risk Probability</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{allocation["risk_probability"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Debate
    st.markdown('<div class="section-title">Structured Agent Exchange</div>', unsafe_allow_html=True)
    st.write(debate)

# ---------- Footer ----------
st.markdown("""
<hr>
<div style='text-align:center;color:#64748B;font-size:13px'>
AIC-DAO • Autonomous Capital Evaluation Infrastructure • v3.0
</div>
""", unsafe_allow_html=True)
