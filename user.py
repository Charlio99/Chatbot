from Graph.readGraph import Decision


class User:
    def __init__(self, cid, step=0, cp=None, latitude=None, longitude=None):
        self.chatId = cid
        self.step = step
        self.lastStep = step
        self.cp = cp
        self.latitude = latitude
        self.longitude = longitude
        self.aux_node = 0

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

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def set_node(self, aux):
        self.aux_node = aux

    def get_node(self):
        return Decision.getInstance().graph.nodes[self.aux_node]['node']

    def __eq__(self, other):
        return self.chatId == other.chatId
