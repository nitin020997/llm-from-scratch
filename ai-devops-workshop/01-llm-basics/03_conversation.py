"""
task — Multi-turn Conversation (Chat Memory)
------------------------------------------------
Concept: Claude has no memory between separate API calls.
To have a conversation, you must send the full history
of messages every time.

This is the foundation of every chatbot and AI agent:
  messages = [
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "user",      "content": "..."},  <-- new question
  ]
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SRE_SYSTEM_PROMPT = """You are an expert SRE assistant. Be concise and actionable.
Think in terms of: observe → diagnose → fix → verify."""

def chat():
    history = []

    print("SRE Chat Assistant (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SRE_SYSTEM_PROMPT,
            messages=history
        )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})

        print(f"\nClaude: {reply}\n")

if __name__ == "__main__":
    chat()
