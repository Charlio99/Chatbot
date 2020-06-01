from py2neo.ogm import GraphObject, Property, RelatedTo


class User(GraphObject):
    __primarykey__ = "chatId"

    name = Property()
    chatId = Property()
    last_step = Property()

    lives = RelatedTo("Location", "LIVES")
    likes = RelatedTo("Category", "LIKES")
    went = RelatedTo("Place", "WENT_TO")


class Location(GraphObject):
    latitude = Property()
    longitude = Property()


class Category(GraphObject):
    __primarykey__ = "categoryName"
    visibleName = Property()
    categoryName = Property()


class Place(GraphObject):
    __primarykey__ = "placeName"
    placeName = Property()
    locatedIn = RelatedTo("Location", "LOCATED_IN")
    category = RelatedTo("Category", "HAS_CATEGORY")
