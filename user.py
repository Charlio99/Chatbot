from Graph.readGraph import Decision


class User:

    def __init__(self, cid, step=0, cp=None, city=None, email=None, name=None):
        self.chatId = cid
        self.step = step
        self.lastStep = step
        self.cp = cp
        self.aux_node = 0
        self.city = city
        self.email = email
        self.name = name

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

    def set_node(self, aux):
        self.aux_node = aux

    def get_node(self):
        return Decision.getInstance().graph.nodes[self.aux_node]['node']

    def __eq__(self, other):
        return self.chatId == other.chatId

    def get_city(self):
        return self.city

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name
