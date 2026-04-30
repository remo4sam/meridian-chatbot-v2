---
title: Meridian Chatbot
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Meridian Electronics AI Support Chatbot (Enhanced)

## Features
- MCP Tool Auto-discovery
- Streaming responses
- Session memory + summarization
- Retry + fallback handling
- Logging + trace IDs

## Run
pip install -r requirements.txt
cp .env.example .env
python app/main.py
