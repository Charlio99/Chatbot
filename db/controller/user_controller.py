from py2neo import NodeMatcher

from graph.read_graph import Decision
from db.connection import Connection
from db.model.models import User, Location


class UserController:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if UserController.__instance is None:
            UserController()
        return UserController.__instance

    def __init__(self):
        self.graph = Connection.get_instance().getConnection()
        self.nodes = NodeMatcher(self.graph)
        UserController.__instance = self

    def store_user(self, cid, name, step, node=0):
        """
        Stores the user
        :param node:
        :param step:
        :param cid:
        :param name:
        :return: The user neo4j class type
        """
        p = User()
        p.name = name
        p.chat_id = cid
        p.step = step
        p.node = node
        self.graph.push(p)
        return p

    def get_user_location_by_user_id(self, chat_id):
        user = User.match(self.graph, chat_id).first()
        try:
            loc = user.lives._related_objects[0][0]
        except IndexError:
            loc = Location()
        return loc

    def get_user_by_id(self, chat_id):
        return User.match(self.graph, chat_id).first()

    def check_user_by_id_if_exists(self, chat_id):
        return User.match(self.graph, chat_id).first() is None

    def store_step(self, user, step):
        user.step = step
        self.graph.push(user)

    def get_node(self, chat_id):
        node = self.get_instance().getUserById(chat_id).node
        return Decision.get_instance().graph.nodes[node]['node']

    def save_node(self, user, node):
        user.node = node
        self.graph.push(user)

    def save_location(self, user, lat, long):
        exists = self.get_instance().getUserLocationByUserID(user.chat_id)
        if exists.latitude is None or exists.longitude is None:
            loc = Location()
            loc.longitude = long
            loc.latitude = lat
            user.lives.add(loc)
            self.graph.push(user)
        else:
            exists.latitude = lat
            exists.longitude = long
            self.graph.push(exists)
