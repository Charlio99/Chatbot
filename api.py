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


def nearby_places(lat, long, category, radius=None):
    rank_by = 'distance'
    result = gmaps.places_nearby(location=(lat, long), radius=radius, open_now=True, type=category,
                                     rank_by=rank_by)
    if result is not None:
        loc = result.get('results')[0].get('geometry').get('location')
        location = (loc.get('lat'), loc.get('lng'))
        return location
    else:
        return None
