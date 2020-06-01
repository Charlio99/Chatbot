from py2neo import Graph


class Connection:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    """Constructor"""
    def __init__(self):
        """ Virtually private constructor. """
        self._driver = None
        if Connection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.graph = Graph("bolt://localhost:7687", auth=('neo4j', "bitnami"))
            Connection.__instance = self

    def getConnection(self):
        return self.graph

    def close(self):
        self._driver.close()