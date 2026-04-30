import json
import time

import requests

from logger import get_logger


class MCPClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        self._id = 0

    def _rpc(self, method, params=None):
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            payload["params"] = params

        res = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
        res.raise_for_status()

        if "text/event-stream" in res.headers.get("content-type", ""):
            data = self._parse_sse(res.text)
        else:
            data = res.json()

        if "error" in data:
            raise RuntimeError(data["error"].get("message", "rpc error"))
        return data.get("result", {})

    @staticmethod
    def _parse_sse(text):
        for line in text.splitlines():
            if line.startswith("data:"):
                return json.loads(line[5:].strip())
        raise RuntimeError("empty SSE response")

    @staticmethod
    def _extract_text(result):
        content = result.get("content", [])
        return "\n".join(c.get("text", "") for c in content if c.get("type") == "text")

    def list_tools(self):
        try:
            return self._rpc("tools/list")
        except Exception as e:
            return {"error": str(e), "tools": []}

    def get_openai_tools(self):
        result = self.list_tools()
        return [
            {"type": "function", "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("inputSchema", {"type": "object", "properties": {}}),
            }}
            for t in result.get("tools", [])
        ]

    def call_tool(self, name, args, retries=3, trace_id=None):
        log = get_logger(trace_id or "no-trace")
        for i in range(retries):
            try:
                log("INFO", f"MCP call {i+1}: {name}")
                result = self._rpc("tools/call", {"name": name, "arguments": args})
                if result.get("isError"):
                    return {"error": self._extract_text(result) or "tool error"}
                return {"content": self._extract_text(result)}
            except Exception as e:
                log("ERROR", f"{name} failed: {e}")
                time.sleep(0.5 * (2 ** i))
        return {"error": "failed after retries"}
