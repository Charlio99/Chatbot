from py2neo import NodeMatcher, datetime

from db.connection import Connection
from db.model.models import Place, Category, Location, User


class PlacesController:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if PlacesController.__instance is None:
            PlacesController()
        return PlacesController.__instance

    def __init__(self):
        self.graph = Connection.get_instance().get_connection()
        self.nodes = NodeMatcher(self.graph)
        PlacesController.__instance = self

    def create_place(self, place_name, latitude, longitude, address_name, category_name, subcategory_name, user):
        p = Place.match(self.graph, place_name).first()
        if p is None:
            p = Place()
            p.placeName = place_name

        cat = Category.match(self.graph, category_name).first()

        try:
            loc = p.locatedIn._related_objects[0][0]
        except IndexError:
            loc = Location()
            loc.latitude = latitude
            loc.longitude = longitude

        p.locatedIn.add(loc, properties={'AdressName': address_name})
        p.category.add(cat, properties={'subcategory': subcategory_name})
        self.graph.push(p)
        user.went.add(p, properties={'Date': datetime.now()})
        self.graph.push(user)

    def recommendation(self, subcategory, user_id):
        results = []
        for user in list(User.match(self.graph).where(chatId=user_id)):
            for went in sorted(user.went._related_objects, key=lambda element: element[1]['Date'], reverse=True):
                if went[0].category._related_objects[0][0].categoryName == subcategory:
                    sublist = []
                    sublist.append(went[0])
                    sublist.append(went[1])
                    results.append(sublist)

        return results[:3]

    def get_place_by_name(self, place_name):
        return Place.match(self.graph, place_name).first()
