
import os
from dotenv import load_dotenv
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
