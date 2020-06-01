import neotime
from py2neo import NodeMatcher

from neo4jDB.Connection import Connection
from neo4jDB.Models.models import Place, Category, Location, User


class PlacesController:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PlacesController.__instance is None:
            PlacesController()
        return PlacesController.__instance

    def __init__(self):
        self.graph = Connection.get_instance().getConnection()
        self.nodes = NodeMatcher(self.graph)
        PlacesController.__instance = self

    def createPlace(self, placename, latiutude, longitude, adressName, categoryname, subcategoryName, user):
        p = Place.match(self.graph, placename).first()
        if p is None:
            p = Place()
            p.placeName = placename

        cat = Category.match(self.graph, categoryname).first()

        try:
            l = p.locatedIn._related_objects[0][0]
        except IndexError:
            l = Location()
            l.latitude = latiutude
            l.longitude = longitude

        p.locatedIn.add(l, properties={'AdressName': adressName})
        p.category.add(cat, properties={'subcategory': subcategoryName})
        self.graph.push(p)
        user.went.add(p, properties={'Date': neotime.DateTime.now()})
        self.graph.push(user)


    def recomendation(self, subcategory, user_id):
        results = []
        for user in list(User.match(self.graph).where(chatId=user_id)):
            for went in sorted(user.went._related_objects, key=lambda element: element[1]['Date'], reverse=True):
                if went[0].category._related_objects[0][0].categoryName == subcategory:
                    sublist = []
                    sublist.append(went[0])
                    sublist.append(went[1])
                    results.append(sublist)

        return results[:3]

    def getPlaceByName(self, placename):
        return Place.match(self.graph, placename).first()
