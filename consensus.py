def calculate_confidence(risk_score, market_score, capital_score):
    """
    Weighted confidence aggregation.
    Institutional weighting logic:
    Risk > Market > Capital
    """

    w_risk = 0.4
    w_market = 0.35
    w_capital = 0.25

    confidence = (
        (risk_score * w_risk) +
        (market_score * w_market) +
        (capital_score * w_capital)
    )

    return round(confidence, 3)


def capital_allocation(confidence, treasury=1000000):
    """
    Treasury-aware dynamic capital allocation.
    Allocation scales proportionally with confidence.
    Includes structured deployment logic.
    """

    # Dynamic scaling (max 30% of treasury)
    max_deploy_ratio = 0.30
    allocation = int(confidence * treasury * max_deploy_ratio)

    risk_probability = round(1 - confidence, 2)

    # Decision tiers
    if confidence < 0.40:
        decision = "Capital Preservation"
        structure = "No allocation. Monitor quarterly."

    elif 0.40 <= confidence < 0.60:
        decision = "Pilot Tranche"
        structure = "Milestone-gated release (Proof-of-Execution required)"

    elif 0.60 <= confidence < 0.80:
        decision = "Structured Investment"
        structure = "40% upfront, 30% MVP validation, 30% revenue milestone"

    else:
        decision = "High Conviction Deployment"
        structure = "60% upfront, 40% milestone-based governance release"

    return {
        "decision": decision,
        "allocation": allocation,
        "structure": structure,
        "risk_probability": risk_probability
    }
