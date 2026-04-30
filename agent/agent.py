import json

from core.llm import call_llm, mcp_client
from logger import get_logger


def run_agent_stream(messages, session, trace_id):
    log = get_logger(trace_id)
    resp = call_llm(messages)
    msg = resp.choices[0].message

    if msg.tool_calls:
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": t.id,
                    "type": "function",
                    "function": {
                        "name": t.function.name,
                        "arguments": t.function.arguments,
                    },
                }
                for t in msg.tool_calls
            ],
        })

        for t in msg.tool_calls:
            name = t.function.name
            args = json.loads(t.function.arguments)
            session.update_intent(name)
            log("INFO", f"Tool {name} {args}")

            result = mcp_client.call_tool(name, args, trace_id=trace_id)
            content = result.get("error") or result.get("content", "")

            messages.append({
                "role": "tool",
                "tool_call_id": t.id,
                "content": content,
            })

        yield from run_agent_stream(messages, session, trace_id)
        return

    text = msg.content or ""
    buf = ""
    for c in text:
        buf += c
        yield buf
