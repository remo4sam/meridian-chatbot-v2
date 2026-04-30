
def build_system_prompt(session):
    return f"""
Assistant for Meridian Electronics.

Authenticated: {session.authenticated}
User: {session.user_id}
Intent: {session.memory.get("last_intent")}

Rules:
- Use tools
- No hallucination
"""
