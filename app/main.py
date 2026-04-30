import gradio as gr

from agent.agent import run_agent_stream
from agent.session import SessionState
from core.prompts import build_system_prompt
# from logger import setup_logger, generate_trace_id
from agents import trace, gen_trace_id

trace_id = gen_trace_id()
# setup_logger()
session = SessionState()


def chat(user_input, history):
    # trace_id=generate_trace_id()
    messages = [{"role": "system", "content": build_system_prompt(session)}]

    for u, a in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})

    messages.append({"role": "user", "content": user_input})
    messages = messages[:1] + messages[-10:]

    stream = run_agent_stream(messages, session, trace_id)
    history.append((user_input, ""))

    for chunk in stream:
        history[-1] = (user_input, chunk)
        yield history, history


with gr.Blocks() as demo:
    gr.Markdown("# Meridian Bot v2")
    chatbox = gr.Chatbot()
    inp = gr.Textbox()
    inp.submit(chat, [inp, chatbox], [chatbox, chatbox])

demo.launch()
