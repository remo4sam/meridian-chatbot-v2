import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import chainlit as cl

from agent.agent import run_agent_stream
from agent.session import SessionState
from core.prompts import build_system_prompt
from agents import gen_trace_id

trace_id = gen_trace_id()
session = SessionState()


@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])


@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    user_input = message.content

    messages = [{"role": "system", "content": build_system_prompt(session)}]
    for u, a in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": user_input})
    messages = messages[:1] + messages[-10:]

    msg = cl.Message(content="")
    await msg.send()

    final = ""
    for chunk in run_agent_stream(messages, session, trace_id):
        final = chunk
        msg.content = chunk
        await msg.update()

    history.append((user_input, final))
    cl.user_session.set("history", history)
