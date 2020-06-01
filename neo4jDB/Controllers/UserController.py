from py2neo import Graph, NodeMatcher

from neo4jDB.Connection import Connection
from neo4jDB.Models.models import User, Location


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

    def storeUser(self, user):
        """
        Stores the user given a user.py class
        :param user:
        :return: The user neo4j class type
        """
        p = User()
        p.name = user.get_name()
        p.chatId = user.get_chat_id()
        p.last_step = user.get_last_step()
        l = Location()
        l.latitude = user.get_longitude()
        l.latitude = user.get_latitude()
        p.lives(l)
        self.graph.push(p)
        return p

    def getUserLocationByUserID(self, chatId):
        user = User.match(self.graph, chatId).first()
        return user.lives._related_objects[0][0]

    def getLocationByUserClass(self, user):
        return user.lives.related_class

    def getUserById(self, chatId):
        return User.match(self.graph, chatId).first()

    def checkUserByIdIfExists(self, chatId):
        return User.match(self.graph, chatId).first() is None

    def storeStep(self, user, step):
        user.last_step = step
        self.graph.push(user)
