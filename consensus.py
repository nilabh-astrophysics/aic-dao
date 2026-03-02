import math

# ---------------- NORMALIZATION ----------------

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(value, max_value))

# ---------------- RISK SCORE ----------------

def risk_score(raised, burn, runway, revenue_status):
    if burn == 0:
        burn_ratio = 0
    else:
        burn_ratio = burn / raised if raised > 0 else 1

    runway_score = clamp(runway / 24)  # 24 months ideal runway
    burn_score = clamp(1 - burn_ratio)
    revenue_bonus = 0.1 if revenue_status.lower() != "pre-revenue" else 0

    score = (0.5 * runway_score) + (0.4 * burn_score) + revenue_bonus
    return clamp(score)

# ---------------- MARKET SCORE ----------------

def market_score(runway, revenue_status, traction_text):
    traction_factor = 0.5
    if "user" in traction_text.lower():
        traction_factor += 0.1
    if "revenue" in revenue_status.lower():
        traction_factor += 0.15

    runway_factor = clamp(runway / 18)

    score = (0.6 * traction_factor) + (0.4 * runway_factor)
    return clamp(score)

# ---------------- CAPITAL STRUCTURE SCORE ----------------

def capital_structure_score(raised, burn, runway):
    efficiency = clamp((raised - (burn * runway)) / raised if raised > 0 else 0)
    runway_factor = clamp(runway / 18)

    score = (0.6 * efficiency) + (0.4 * runway_factor)
    return clamp(score)

# ---------------- CONFIDENCE AGGREGATION ----------------

def calculate_confidence(risk, market, capital):
    return round((0.40 * risk) + (0.35 * market) + (0.25 * capital), 3)

# ---------------- CAPITAL ALLOCATION ENGINE ----------------

def capital_allocation(confidence):
    if confidence < 0.4:
        return {
            "decision": "Capital Preservation Mode",
            "allocation": 50000,
            "structure": "Milestone-based staged release",
            "risk_probability": round(1 - confidence, 2)
        }

    elif confidence < 0.6:
        return {
            "decision": "Controlled Pilot Deployment",
            "allocation": 100000,
            "structure": "Tranche-based allocation",
            "risk_probability": round(1 - confidence, 2)
        }

    elif confidence < 0.8:
        return {
            "decision": "Structured Investment",
            "allocation": 150000,
            "structure": "Phased capital release with performance checkpoints",
            "risk_probability": round(1 - confidence, 2)
        }

    else:
        return {
            "decision": "High Conviction Deployment",
            "allocation": 250000,
            "structure": "Full allocation with governance oversight",
            "risk_probability": round(1 - confidence, 2)
        }
