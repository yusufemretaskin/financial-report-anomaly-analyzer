import os
import json
from openai import OpenAI

token = os.getenv("GITHUB_TOKEN")

client=OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=token
)

model_name = "openai/gpt-4o-mini"


def generate_anomaly_summary(anomalies: list[dict]) -> str:
    if not anomalies:
        return "No anomalies were detected in the financial report."

    prompt = f"""
You are a financial reporting assistant.

Explain the following detected anomalies in simple business language.
Do not invent extra information.

Anomalies:
{json.dumps(anomalies, indent=2)}
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You explain financial report anomalies clearly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content