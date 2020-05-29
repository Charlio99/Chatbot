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
