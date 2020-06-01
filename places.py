from enum import Enum


class Food(Enum):
    RESTAURANT = 'restaurant'
    BAKERY = 'bakery'
    CAFE = 'cafe'
    BAR = 'bar'
    MEAL_TAKEAWAY = 'meal_takeaway'


class Store(Enum):
    BOOK = 'book_store'
    CLOTHES = 'clothing_store'
    DEPARTMENT = 'department_store'
    JEWELRY = 'jewelry_store'
    SHOE = 'shoe_store'
    SHOPPING_MALL = 'shopping_mall'
    STORE = 'store'


class Entertainment(Enum):
    BOWLING = 'bowling_alley'
    CASINO = 'casino'
    CINEMA = 'movie_theater'
    MUSEUM = 'museum'
    NIGHT_CLUB = 'night_club'
    STADIUM = 'stadium'
    AQUARIUM = 'aquarium'
    ART_GALLERY = 'art_gallery'
    ZOO = 'zoo'


class Health(Enum):
    PARK = 'park'
    SPA = 'spa'
    GYM = 'gym'
    HAIR_CARE = 'hair_care'
    BEAUTY_SALON = 'beauty_salon'


class Tourism(Enum):
    MUSEUM = 'museum'
    ART_GALLERY = 'art_gallery'
    TOURIST_ATTRACTION = 'tourist_attraction'
    ZOO = 'zoo'
    PARK = 'park'


class Places:
    __instance = None

    @staticmethod
    def getInstance():
        if Places.__instance is None:
            Places()
        return Places.__instance

    def __init__(self):  # Declare the constructor with or without parameters

        Places.__instance = self
        self.names = {
            'restaurant': 'restaurante',
            'cafe': 'café',
            'bakery': 'pastelería',
            'meal_takeaway': 'take away',
            'book_store': 'librería',
            'clothing_store': 'tienda de ropa',
            'department_store': 'almacén',
            'jewelry_store': 'tienda de ropa',
            'shoe_store': 'tienda de zapatos',
            'shopping_mall': 'centro comercial',
            'store': 'tienda',
            'bowling_alley': 'bolera',
            'movie_theater': 'cine',
            'museum': 'museo',
            'night_club': 'club nocturno',
            'stadium': 'estadio',
            'aquarium': 'acuario',
            'art_gallery': 'galería de arte',
            'park': 'parque',
            'hair_care': 'peluquería',
            'beauty_salon': 'salón de belleza',
            'tourist_attraction': 'atracción turística'
        }

    def get_place_name(self, key):

        if key in self.names:
            return self.names[key]

        return key
