import streamlit as st
import plotly.graph_objects as go
import time
import datetime
from agents import run_agent, simulate_debate
from consensus import (
    risk_score,
    market_score,
    capital_structure_score,
    calculate_confidence,
    capital_allocation
)

st.set_page_config(page_title="AIC-DAO", layout="wide")

# -------------------- STYLING --------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0B1120;
    font-family: 'Inter', sans-serif;
}

.hero-title {
    font-size: 44px;
    font-weight: 700;
    margin-top: 20px;
}

.meta {
    font-size: 12px;
    color: #64748B;
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
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
    padding: 30px;
    border-radius: 10px;
    margin-top: 20px;
}

.transcript-box {
    background-color: #0F172A;
    border-left: 4px solid #22C55E;
    padding: 25px;
    border-radius: 8px;
    margin-top: 20px;
}

.footer {
    text-align:center;
    font-size:13px;
    color:#475569;
    margin-top:70px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="hero-title">AIC-DAO</div>', unsafe_allow_html=True)
st.markdown('<div class="meta">Autonomous Institutional Capital Evaluation Infrastructure</div>', unsafe_allow_html=True)

evaluation_id = f"AIC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
timestamp = datetime.datetime.now().strftime("%d %b %Y | %H:%M")

st.markdown(
    f'<div class="meta">Evaluation ID: {evaluation_id} | Timestamp: {timestamp}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------- MODE --------------------
mode = st.radio("Evaluation Mode", ["Startup", "Public Company"], horizontal=True)

# -------------------- INPUT SECTION --------------------
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

# -------------------- RUN EVALUATION --------------------
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

    with st.spinner("Executing multi-agent capital assessment..."):
        time.sleep(0.6)

        # Qualitative agent analysis (text only)
        risk = run_agent("Risk Analyst", entity_data)
        market = run_agent("Market Analyst", entity_data)
        capital = run_agent("Capital Structure Analyst", entity_data)

        # ---------------- QUANTITATIVE SCORES ----------------
        risk_val = risk_score(raised, burn, runway, revenue)
        market_val = market_score(runway, revenue, traction)
        capital_val = capital_structure_score(raised, burn, runway)

        confidence = calculate_confidence(
            risk_val,
            market_val,
            capital_val
        )

        allocation = capital_allocation(confidence)
        debate = simulate_debate(risk, market)

    # -------------------- RESOLUTION --------------------
    st.markdown('<div class="resolution-box">', unsafe_allow_html=True)

    st.markdown(f"### {allocation['decision']}")
    st.markdown(f"**Recommended Allocation:** ${allocation['allocation']:,}")
    st.markdown(f"**Deployment Structure:** {allocation['structure']}")
    st.markdown(f"**Downside Risk Probability:** {allocation['risk_probability']}")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------- CONFIDENCE GAUGE --------------------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range': [0, 1]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    # -------------------- SCORE BREAKDOWN --------------------
    st.markdown('<div class="section-title">Score Breakdown</div>', unsafe_allow_html=True)

    st.markdown('<div class="breakdown-box">', unsafe_allow_html=True)

    st.markdown("### Agent Scores (0 – 1 Scale)")
    st.write(f"Risk Score: {risk_val}")
    st.write(f"Market Score: {market_val}")
    st.write(f"Capital Structure Score: {capital_val}")
    st.write(f"Weighted Confidence: {confidence}")

    st.markdown("---")

    st.markdown("### Aggregation Formula")
    st.markdown("""
    Confidence =  
    (0.40 × Risk Score) +  
    (0.35 × Market Score) +  
    (0.25 × Capital Structure Score)
    """)

    st.markdown("---")

    st.markdown("### Scoring Interpretation")
    st.markdown("""
    **0.0 – 0.4** → High structural risk / capital preservation  
    **0.4 – 0.6** → Moderate uncertainty / controlled pilot deployment  
    **0.6 – 0.8** → Sustainable growth profile / structured allocation  
    **0.8 – 1.0** → Strong capital efficiency & defensibility  
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------- DELIBERATION TRANSCRIPT --------------------
    st.markdown('<div class="section-title">Internal Committee Deliberation Log</div>', unsafe_allow_html=True)

    st.markdown('<div class="transcript-box">', unsafe_allow_html=True)

    st.markdown("**Round 1 — Risk Concerns**")
    st.write(risk["analysis"])

    st.markdown("**Round 1 — Market Response**")
    st.write(market["analysis"])

    st.markdown("**Round 2 — Risk Escalation**")
    st.write("Risk committee further evaluates capital durability and scaling exposure.")

    st.markdown("**Round 2 — Market Defense**")
    st.write("Market analyst reinforces growth trajectory and structural demand indicators.")

    st.markdown("**Final Committee Statement**")
    st.write(debate)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown(
    "<div class='footer'>AIC-DAO • Institutional Autonomous Capital Infrastructure • v7.0 Quantitative</div>",
    unsafe_allow_html=True
)
