
class SessionState:
    def __init__(self):
        self.authenticated=False
        self.user_id=None
        self.memory={"context":{}, "last_intent":None}

    def set_auth(self, uid):
        self.authenticated=True
        self.user_id=uid

    def update_intent(self, intent):
        self.memory["last_intent"]=intent
