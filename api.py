import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDnzTNT7BFpAy-7E1aaCJrwxYFkhaBKCgo')

"""
def places_nearby(
    client,
    location=None,
    radius=None,
    keyword=None,
    language=None,
    min_price=None,
    max_price=None,
    name=None,
    open_now=False,
    rank_by=None,
    type=None,
    page_token=None,
):
"""


def nearby_places(lat, long, category, radius=1500):
    result = gmaps.places_nearby(location=(lat, long), radius=radius, open_now=True, type=category.value,
                                 rank_by='distance')
    if result is not None:
        return result.get('results')
    else:
        return None
