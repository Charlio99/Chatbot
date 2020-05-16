class User:
    def __init__(self, cid, step=0, cp=None):
        self.chatId = cid
        self.step = step
        self.lastStep = step
        self.cp = cp

    def get_chat_id(self):
        return self.chatId

    def set_chat_id(self, cid):
        self.chatId = cid

    def get_step(self):
        return self.step

    def get_last_step(self):
        return self.lastStep

    def set_step(self, step):
        self.lastStep = self.step
        self.step = step

    def get_postal_code(self):
        return self.cp

    def set_postal_code(self, cp):
        self.cp = cp

    def __eq__(self, other):
        return self.chatId == other.chatId
