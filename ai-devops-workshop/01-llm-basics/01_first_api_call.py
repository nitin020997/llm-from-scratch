"""
Simple example: make one Anthropics/LLM API call and print the reply.

Concept: send a prompt, receive the model response, and handle it.
This file is a minimal, inspirational example rather than a verbatim
tutorial excerpt.
"""

import os
import anthropic
import sys
from dotenv import load_dotenv

load_dotenv()

# Validate API key early and give a helpful message if missing or placeholder
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key.strip() == "your_real_api_key_here":
    print(
        "Missing or placeholder API key: set ANTHROPIC_API_KEY in your .env or environment."
    )
    sys.exit(1)

client = anthropic.Anthropic(api_key=api_key)

def ask_model(question: str) -> str:
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": question}],
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        print("Authentication failed: check your ANTHROPIC_API_KEY and try again.")
        raise
    except Exception as e:
        print(f"Request failed: {e}")
        raise

if __name__ == "__main__":
    question = "What is Kubernetes in one sentence?"
    print(f"Question: {question}\n")
    answer = ask_model(question)
    print(f"Model response:\n{answer}")
