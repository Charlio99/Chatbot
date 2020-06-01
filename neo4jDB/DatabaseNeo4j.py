from py2neo import Graph, Node, Relationship, NodeMatcher
import os


class DatabaseNeo4j(object):
    __instance = None

    def close(self):
        self._driver.close()

    """Constructor"""

    def __init__(self):
        """ Virtually private constructor. """
        self._driver = None
        if DatabaseNeo4j.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.graph = Graph("bolt://localhost:7687", auth=('neo4j', "bitnami"))
            DatabaseNeo4j.__instance = self
            self.matcher = NodeMatcher(self.graph)

    def storeUserInDatabase(self, user):
        user.get_postal_code()

    def _create_and_return_user(self, user):
        tx = self.graph.begin()
        userNeo4j = Node("User", name=user.get_name(), email=user.get_email())
        user_id = userNeo4j.identity
        tx.create(userNeo4j)
        postalcode = self.matcher.match("PostalCode", City=user.get_city(), PostalCode=user.get_postal_code()).first()
        # we create the new postal code node matching with the correct city and postal code
        if postalcode is None:
            postalcode = Node("PostalCode", City=user.get_city(), PostalCode=user.get_postal_code())
            tx.create(postalcode)
        viu = Relationship(userNeo4j, "LIVES_IN", postalcode)
        tx.create(viu)
        tx.commit()
        return user_id

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DatabaseNeo4j.__instance is None:
            DatabaseNeo4j()
        return DatabaseNeo4j.__instance

    def check_user_if_exists(self, user):
        return self.matcher.match("User", name=user.get_name(), email=user.get_email()) is None

    def return_user_details(self, user):
        return self.matcher.match("User", name=user.get_name(), email=user.get_email()).first()

