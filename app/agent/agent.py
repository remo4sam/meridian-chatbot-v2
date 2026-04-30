
import json
from core.llm import call_llm, mcp
from logger import get_logger

def summarize(name,res):
    if "error" in res: return f"{name} failed"
    return f"{name} ok"

def fallback(name):
    return f"{name} unavailable, try later."

def run_agent_stream(messages, session, trace_id):
    log=get_logger(trace_id)
    resp=call_llm(messages)
    msg=resp.choices[0].message

    if msg.tool_calls:
        for t in msg.tool_calls:
            name=t.function.name
            args=json.loads(t.function.arguments)
            session.update_intent(name)

            log("INFO", f"Tool {name} {args}")
            result=mcp.call_tool(name,args,trace_id=trace_id)

            if "error" in result:
                yield fallback(name)
                return

            messages.append({
                "role":"tool","tool_name":name,
                "content":summarize(name,result)
            })

        yield from run_agent_stream(messages,session,trace_id)
        return

    text=msg.content or ""
    buf=""
    for c in text:
        buf+=c
        yield buf
