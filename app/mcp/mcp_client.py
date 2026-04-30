
import requests, time

class MCPClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def list_tools(self):
        try:
            return requests.get(f"{self.base_url}/tools").json()
        except Exception as e:
            return {"error": str(e)}

    def get_openai_tools(self):
        tools = self.list_tools()
        return [
            {"type":"function","function":{
                "name":t["name"],
                "description":t.get("description",""),
                "parameters":t.get("input_schema",{"type":"object","properties":{}})
            }}
            for t in tools.get("tools",[])
        ]

    def call_tool(self, name, args, retries=3, trace_id=None):
        from app.logger import get_logger
        log = get_logger(trace_id or "no-trace")

        for i in range(retries):
            try:
                log("INFO", f"MCP call {i+1}: {name}")
                res = requests.post(f"{self.base_url}/call",
                    json={"tool":name,"arguments":args}, timeout=10)
                res.raise_for_status()
                return res.json()
            except Exception as e:
                log("ERROR", f"{name} failed: {e}")
                time.sleep(0.5*(2**i))
        return {"error":"failed after retries"}
