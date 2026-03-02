def calculate_confidence(risk_score, market_score, token_score):
    w_risk = 0.4
    w_market = 0.35
    w_token = 0.25

    confidence = (
        (risk_score * w_risk) +
        (market_score * w_market) +
        (token_score * w_token)
    )

    return round(confidence, 2)


def capital_allocation(confidence, treasury=1000000):

    if confidence < 0.4:
        return {
            "decision": "Reject",
            "allocation": 0,
            "structure": "No funding",
            "risk_probability": round(1 - confidence, 2)
        }

    elif 0.4 <= confidence < 0.6:
        amount = treasury * 0.05
        return {
            "decision": "Pilot Tranche",
            "allocation": int(amount),
            "structure": "Milestone-gated release",
            "risk_probability": round(1 - confidence, 2)
        }

    elif 0.6 <= confidence < 0.8:
        amount = treasury * 0.15
        return {
            "decision": "Structured Investment",
            "allocation": int(amount),
            "structure": "40% upfront, 30% MVP, 30% revenue milestone",
            "risk_probability": round(1 - confidence, 2)
        }

    else:
        amount = treasury * 0.25
        return {
            "decision": "High Conviction Deployment",
            "allocation": int(amount),
            "structure": "60% upfront, 40% milestone-based",
            "risk_probability": round(1 - confidence, 2)
        }