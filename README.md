# llm-from-scratch

A small, practical repo showing how to call an LLM API from Python with a clean, task-oriented example.

This repository includes:

- `ai-devops-workshop/01-llm-basics/01_first_api_call.py`
  - single-call example with API key validation and generic model helper naming.
- `ai-devops-workshop/01-llm-basics/02_sre_context.py`
  - example system prompt for a DevOps/SRE-style assistant.
- `ai-devops-workshop/01-llm-basics/03_conversation.py`
  - multi-turn chat example with conversation history.

## Getting started

1. Create a `.env` file with your Anthropics key:
   ```env
   ANTHROPIC_API_KEY=your_real_api_key_here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the example:
   ```bash
   python ai-devops-workshop/01-llm-basics/01_first_api_call.py
   ```

## Notes

- The code intentionally avoids copy-style "episode" wording and uses a simple task-oriented naming style.
- `01_first_api_call.py` demonstrates minimal request/response flow and graceful API key validation.

## LinkedIn post draft

Copy this post to share the repo:

```text
I just launched `llm-from-scratch` — a compact Python repo showing how to call an LLM API cleanly, without tutorial jargon.

It includes:
- a minimal single-call example with API key validation
- a DevOps/SRE system prompt example
- a multi-turn chat example with conversation history

If you want a simple, task-oriented reference for building LLM integrations, check it out:
https://github.com/nitin020997/llm-from-scratch

#ai #LLM #Python #DevOps
```
