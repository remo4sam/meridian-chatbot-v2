---
title: Meridian Chatbot
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Meridian Electronics AI Support Chatbot

<blockquote>
<h1>🚨 LIVE DEMO HAS MOVED 🚨</h1>
<h2>✅ NEW URL → <a href="https://huggingface.co/spaces/remosamuelpaul/meridian-chatbot" target="_blank" rel="noopener noreferrer">https://huggingface.co/spaces/remosamuelpaul/meridian-chatbot</a></h2>
<h2>❌ OLD URL (DO NOT USE) → <s><a href="https://c5t6r3lwt3mzxd5c4bqabszqze0pgexv.lambda-url.eu-west-1.on.aws/" target="_blank" rel="noopener noreferrer">https://c5t6r3lwt3mzxd5c4bqabszqze0pgexv.lambda-url.eu-west-1.on.aws/</a></s></h2>
<p>The previously submitted AWS Lambda URL is <strong>deprecated and no longer working</strong> — Lambda Function URLs do not support the WebSocket connections Chainlit needs. The chatbot now runs on <strong>Hugging Face Spaces</strong> at the URL above. Please update any bookmarks or submissions.</p>
</blockquote>

## Features
- Chainlit chat UI with streaming responses
- MCP tool auto-discovery over JSON-RPC (`tools/list`, `tools/call`)
- Tool-calling loop with proper OpenAI `tool_call_id` round-tripping
- Session memory + intent tracking
- Retry with exponential backoff on MCP calls
- Logging with trace IDs

## Project layout
```
main.py              Chainlit entrypoint
agent/agent.py       Tool-calling loop
core/llm.py          OpenAI client + MCP wiring
core/prompts.py      System prompt
meridian_mcp/client.py  JSON-RPC MCP client
```

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENAI_API_KEY, MCP_SERVER_URL, MODEL
chainlit run main.py
```

## Run with Docker
```bash
docker build -t meridian-chatbot .
docker run --rm -p 7860:7860 --env-file .env meridian-chatbot
```

## Environment variables
| Name | Description |
|------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `MCP_SERVER_URL` | MCP server endpoint (JSON-RPC over HTTP) |
| `MODEL` | OpenAI model id (default `gpt-4o-mini`) |

## Deploy to Hugging Face Spaces
The `Dockerfile` and the YAML frontmatter above are all HF needs. Push to your Space remote:
```bash
git remote add hf https://huggingface.co/spaces/<user>/<space>
git push hf main
```
Set `OPENAI_API_KEY`, `MCP_SERVER_URL`, and `MODEL` as secrets in the Space settings.
