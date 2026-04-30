
from openai import OpenAI
from core.config import OPENAI_API_KEY, MODEL, MCP_SERVER_URL
from mcp.mcp_client import MCPClient

client=OpenAI(api_key=OPENAI_API_KEY)
mcp=MCPClient(MCP_SERVER_URL)

def call_llm(messages):
    tools=mcp.get_openai_tools()
    return client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools)
