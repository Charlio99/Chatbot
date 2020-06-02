from py2neo import Graph, NodeMatcher

from Graph.readGraph import Decision
from db.Connection import Connection
from db.Models.models import User, Location


class UserController:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserController.__instance is None:
            UserController()
        return UserController.__instance

    def __init__(self):
        self.graph = Connection.get_instance().getConnection()
        self.nodes = NodeMatcher(self.graph)
        UserController.__instance = self

    def storeUser(self, cid, name, step, node=0):
        """
        Stores the user given a user.py class
        :param node:
        :param step:
        :param cid:
        :param name:
        :return: The user neo4j class type
        """
        p = User()
        p.name = name
        p.chatId = cid
        p.step = step
        p.node = node
        self.graph.push(p)
        return p

    def getUserLocationByUserID(self, chatId):
        user = User.match(self.graph, chatId).first()
        try:
            loc = user.lives._related_objects[0][0]
        except IndexError:
            loc = Location()
        return loc

    def getLocationByUserClass(self, user):
        return user.lives.related_class

    def getUserById(self, chatId):
        return User.match(self.graph, chatId).first()

    def checkUserByIdIfExists(self, chatId):
        return User.match(self.graph, chatId).first() is None

    def storeStep(self, user, step):
        user.step = step
        self.graph.push(user)

    def get_node(self, cid):
        node = self.getInstance().getUserById(cid).node
        return Decision.getInstance().graph.nodes[node]['node']

    def save_node(self, user, node):
        user.node = node
        self.graph.push(user)

    def save_location(self, user, lat, long):
        exists = self.getInstance().getUserLocationByUserID(user.chatId)
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
