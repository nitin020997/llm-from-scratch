"""
task — System Prompt: Giving the model a DevOps Role
------------------------------------------------
Concept: The system prompt is a hidden instruction that sets
Claude's behavior for the entire conversation.

For DevOps/SRE use cases you always want Claude to:
  - Give concise, actionable answers
  - Use proper Linux/K8s/cloud terminology
  - Prioritize safety (don't suggest risky commands without caveats)
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SRE_SYSTEM_PROMPT = """You are an expert SRE (Site Reliability Engineer) assistant.
You have deep knowledge of Kubernetes, Linux, CI/CD pipelines, and cloud infrastructure.

Rules you always follow:
- Be concise and actionable — no fluff
- When suggesting commands, flag any that could be destructive
- Think in terms of: observe → diagnose → fix → verify
- Always consider blast radius before suggesting a fix
"""

def ask_sre(question: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SRE_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    scenarios = [
        "A pod is stuck in CrashLoopBackOff. What are the first 3 things I check?",
        "My deployment rolled out but response times doubled. Walk me through diagnosis.",
    ]

    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario}")
        print(f"{'='*60}")
        print(ask_sre(scenario))
