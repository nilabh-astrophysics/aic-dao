import streamlit as st
import plotly.graph_objects as go
import time
from agents import run_agent, simulate_debate
from consensus import calculate_confidence, capital_allocation

st.set_page_config(page_title="AIC-DAO", layout="wide")

# ---------- Premium CSS + Particle Background ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0E1117;
}

.fade-in {
    animation: fadeIn 1.2s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0px); }
}

.glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 18px;
    color: #9CA3AF;
    margin-bottom: 40px;
}

.gradient-line {
    height:2px;
    background:linear-gradient(90deg,#4F46E5,#06B6D4);
    margin-bottom:20px;
}
</style>

<canvas id="bg"></canvas>

<script>
const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

for (let i = 0; i < 60; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2,
        dx: (Math.random() - 0.5) * 0.5,
        dy: (Math.random() - 0.5) * 0.5
    });
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = "rgba(79,70,229,0.4)";
    particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fill();
        p.x += p.dx;
        p.y += p.dy;
    });
    requestAnimationFrame(draw);
}
draw();
</script>
""", unsafe_allow_html=True)

# ---------- SVG Logo ----------
st.markdown("""
<div class="fade-in" style="display:flex;align-items:center;gap:15px;">
<svg width="34" height="34" viewBox="0 0 24 24" fill="none">
<path d="M5 12C5 8 8 5 12 5C16 5 19 8 19 12" stroke="#4F46E5" stroke-width="2"/>
<path d="M8 14C8 11 10 9 12 9C14 9 16 11 16 14" stroke="#06B6D4" stroke-width="2"/>
</svg>
<div style="font-weight:700;font-size:20px;">AIC-DAO</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title fade-in">Autonomous Capital Infrastructure</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle fade-in">Adaptive Multi-Agent Investment Committee for Web3 Treasuries</div>', unsafe_allow_html=True)

st.markdown('<div class="gradient-line"></div>', unsafe_allow_html=True)

# ---------- Evaluation Mode ----------
mode = st.radio(
    "Evaluation Mode",
    ["Startup", "Public Company"],
    horizontal=True
)

st.markdown("---")

# ---------- Session ----------
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

# ---------- Input Section ----------
if mode == "Startup":
    st.subheader("Startup Evaluation")
else:
    st.subheader("Public Company Evaluation")

name = st.text_input("Entity Name", "FlowBridge")
sector = st.text_input("Sector / Industry", "Cross-chain Liquidity Protocol")
raised = st.number_input("Capital Raised ($)", value=150000)
burn = st.number_input("Monthly Burn ($)", value=20000)
runway = st.number_input("Runway (months)", value=7)
traction = st.text_input("Traction / Market Position", "1200 beta users")
revenue = st.text_input("Revenue Status", "Pre-revenue")
token_model = st.text_input("Governance / Capital Structure", "Governance token")

# ---------- Execution ----------
if st.button("Execute Multi-Agent Capital Review"):

    if mode == "Startup":
        entity_data = f"""
        Name: {name}
        Sector: {sector}
        Raised: {raised}
        Burn: {burn}
        Runway: {runway}
        Traction: {traction}
        Revenue: {revenue}
        Token Model: {token_model}
        Entity Type: Early-Stage Venture
        """
    else:
        entity_data = f"""
        Company: {name}
        Industry: {sector}
        Market Position: {traction}
        Revenue Status: {revenue}
        Capital Structure: {token_model}
        Regulatory Exposure: Moderate
        Entity Type: Public Corporation
        """

    with st.spinner("Deploying Agent Consensus Engine..."):
        st.toast("🧠 Risk Layer Activated")
        time.sleep(0.6)

        if mode == "Startup":
            risk = run_agent("Early-Stage Risk Analyst", entity_data)
            market = run_agent("Startup Market & Moat Analyst", entity_data)
            token = run_agent("Tokenomics & Governance Analyst", entity_data)
        else:
            risk = run_agent("Regulatory & Macro Risk Analyst", entity_data)
            market = run_agent("Competitive Moat & Market Share Analyst", entity_data)
            token = run_agent("Capital Efficiency & Governance Analyst", entity_data)

        confidence = calculate_confidence(risk["score"], market["score"], token["score"])
        allocation = capital_allocation(confidence)
        debate = simulate_debate(risk, market)

    st.session_state.portfolio.append({
        "name": name,
        "confidence": confidence,
        "allocation": allocation["allocation"]
    })

    st.success("Consensus Achieved")

    # ---------- Gauge ----------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis': {'range':[0,1]}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Radar ----------
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[risk["score"], market["score"], token["score"], risk["score"]],
        theta=["Risk","Market","Capital","Risk"],
        fill='toself'
    ))
    radar.update_layout(polar=dict(radialaxis=dict(range=[0,1])), showlegend=False)
    st.plotly_chart(radar, use_container_width=True)

    # ---------- Allocation ----------
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.write("Decision:", allocation["decision"])
    st.write("Recommended Allocation:", f"${allocation['allocation']:,}")
    st.write("Structure:", allocation["structure"])
    st.write("Downside Risk:", allocation["risk_probability"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Debate ----------
    st.subheader("Structured Agent Debate")
    st.write(debate)

# ---------- Footer ----------
st.markdown("""
<hr>
<div style='text-align:center;color:#6B7280;font-size:14px'>
AIC-DAO • Modular Capital Evaluation Infrastructure • Prototype v2.0
</div>
""", unsafe_allow_html=True)
