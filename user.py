class User:
    def __init__(self, cid, step=0, cp=None, latitude=None, longitude=None):
        self.chatId = cid
        self.step = step
        self.cp = cp
        self.latitude = latitude
        self.longitude = longitude

    def get_chat_id(self):
        return self.chatId

    def set_chat_id(self, cid):
        self.chatId = cid

    def get_step(self):
        return self.step

    def set_step(self, step):
        self.step = step

    def get_postal_code(self):
        return self.cp

    def set_postal_code(self, cp):
        self.cp = cp

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def __eq__(self, other):
        return self.chatId == other.chatId
