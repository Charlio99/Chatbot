from py2neo import Graph


class Connection:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._driver = None
        if Connection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.graph = Graph("bolt://byted.duckdns.org:3333", auth=('neo4j', "covid19"))
            Connection.__instance = self

    def get_connection(self):
        return self.graph

    def close(self):
        self._driver.close()
