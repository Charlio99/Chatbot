from py2neo import Graph

from db.connection import Connection
from db.model.models import Category


class DumpDatabaseFile:
    """
    This class is used to dump all the categories to the database
    """

    def __init__(self):
        self.graph = Connection.get_instance().getConnection()

    def dump_database_menu(self):
        condition = False
        while not condition:
            print('Is the database empty? Write yes(y) or no(n)')
            option = input().lower()
            if option == "y":
                print('Dumping database values')
                self.create_categories()
                condition = True
            elif option == "n":
                condition = True
            else:
                print('Input not correct, just write y or n')
                condition = False

    def create_category(self, categoryName):
        cat = Category()
        cat.categoryName = categoryName
        cat.visibleName = categoryName
        self.graph.push(cat)

    def create_categories(self):
        self.create_category('Food')
        self.create_category('Store')
        self.create_category('Entertainment')
        self.create_category('Health')
        self.create_category('Tourism')
