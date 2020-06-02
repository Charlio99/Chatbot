from py2neo import Graph

from db.Connection import Connection
from db.Models.models import Category


class DumpDatabaseFile:
    """
    This class is used to dump all the categories to the database
    """

    def __init__(self):
        self.graph = Connection.get_instance().getConnection()

    def dumpDatabaseMenu(self):
        condition = False
        while not condition:
            print('Is the database empty? Write yes(y) or no(n)')
            option = input().lower()
            if option == "y":
                print('Dumping database values')
                self.createCategories()
                condition = True
            elif option == "n":
                condition = True
            else:
                print('Input not correct, just write y or n')
                condition = False

    def CreateCategory(self, categoryName):
        cat = Category()
        cat.categoryName = categoryName
        cat.visibleName = categoryName
        self.graph.push(cat)

    def createCategories(self):
        self.CreateCategory('Food')
        self.CreateCategory('Store')
        self.CreateCategory('Entertainment')
        self.CreateCategory('Health')
        self.CreateCategory('Tourism')
