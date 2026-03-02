import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from agents import run_agent, simulate_debate
from consensus import calculate_confidence, capital_allocation

st.set_page_config(page_title="AIC-DAO", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0B1120;
    font-family: 'Inter', sans-serif;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    margin-top: 20px;
}

.meta {
    font-size: 12px;
    color: #64748B;
    margin-bottom: 25px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 45px;
    margin-bottom: 15px;
}

.resolution-box {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    padding: 35px;
    border-radius: 12px;
    margin-top: 25px;
}

.breakdown-box {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    padding: 25px;
    border-radius: 10px;
    margin-top: 20px;
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
st.markdown('<div class="meta">Autonomous Capital Evaluation Infrastructure</div>', unsafe_allow_html=True)

evaluation_id = f"AIC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
timestamp = datetime.datetime.now().strftime("%d %b %Y | %H:%M")

st.markdown(
    f'<div class="meta">Evaluation ID: {evaluation_id} | Timestamp: {timestamp}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- Mode ----------
mode = st.radio("Evaluation Mode", ["Startup", "Public Company"], horizontal=True)

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

    with st.spinner("Running multi-agent capital assessment..."):
        time.sleep(0.4)

        risk = run_agent("Risk Analyst", entity_data)
        market = run_agent("Market Analyst", entity_data)
        capital = run_agent("Capital Structure Analyst", entity_data)

        confidence = calculate_confidence(
            risk["score"],
            market["score"],
            capital["score"]
        )

        allocation = capital_allocation(confidence)
        debate = simulate_debate(risk, market)

    # ---------- Resolution ----------
    st.markdown('<div class="resolution-box">', unsafe_allow_html=True)
    st.markdown(f"### {allocation['decision']}")
    st.markdown(f"**Recommended Allocation:** ${allocation['allocation']:,}")
    st.markdown(f"**Deployment Structure:** {allocation['structure']}")
    st.markdown(f"**Downside Risk Probability:** {allocation['risk_probability']}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Confidence Gauge ----------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range':[0,1]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------- Score Breakdown ----------
    st.markdown('<div class="section-title">Score Breakdown</div>', unsafe_allow_html=True)

    st.markdown('<div class="breakdown-box">', unsafe_allow_html=True)
    st.write(f"Risk Score: {risk['score']}")
    st.write(f"Market Score: {market['score']}")
    st.write(f"Capital Structure Score: {capital['score']}")
    st.write(f"Weighted Confidence: {confidence}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Agent Exchange ----------
    st.markdown('<div class="section-title">Structured Agent Exchange</div>', unsafe_allow_html=True)

    st.markdown("**Risk Analyst**")
    st.write(risk["analysis"])

    st.markdown("**Market Analyst**")
    st.write(market["analysis"])

    st.markdown("**Deliberation Outcome**")
    st.write(debate)

# ---------- Footer ----------
st.markdown(
    "<div class='footer'>AIC-DAO • Institutional Autonomous Capital Infrastructure • v5.0</div>",
    unsafe_allow_html=True
)
