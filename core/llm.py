
from openai import OpenAI
from core.config import OPENAI_API_KEY, MODEL, MCP_SERVER_URL
from meridian_mcp.client import MCPClient

client=OpenAI(api_key=OPENAI_API_KEY)
mcp_client=MCPClient(MCP_SERVER_URL)

def call_llm(messages):
    tools=mcp_client.get_openai_tools()
    return client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools)
