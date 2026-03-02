import os
import json
import random

USE_REAL_API = os.getenv("OPENAI_API_KEY") is not None

if USE_REAL_API:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL = "gpt-4o-mini"


def mock_agent(role):
    base_score = round(random.uniform(0.5, 0.85), 2)

    return {
        "score": base_score,
        "key_risks": ["Execution uncertainty", "Market competition"],
        "key_strengths": ["Early traction", "Clear value proposition"],
        "analysis": f"{role} identifies structured upside potential with manageable execution risk."
    }


def run_agent(role, startup_data):

    if not USE_REAL_API:
        return mock_agent(role)

    prompt = f"""
You are acting as the {role} in an Autonomous Investment Committee DAO.

Evaluate this startup:

{startup_data}

Output STRICT JSON:
{{
  "score": 0.0 to 1.0,
  "key_risks": [],
  "key_strengths": [],
  "analysis": ""
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return mock_agent(role)


def simulate_debate(risk_output, market_output):

    if not USE_REAL_API:
        return """
Round 1: Risk Agent questions sustainability.
Round 1: Market Agent defends growth trajectory.

Round 2: Risk Agent raises scaling concerns.
Round 2: Market Agent highlights network effects.

Conclusion: Structured capital deployment recommended.
"""

    debate_prompt = f"""
Simulate 2-round structured debate between:

Risk Agent: {risk_output}
Market Agent: {market_output}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": debate_prompt}],
        temperature=0.6,
    )

    return response.choices[0].message.content