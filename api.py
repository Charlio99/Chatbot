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
    # open_now should be set to True in a production environment, for testing purposes during COVID19 we set it to False
    result = gmaps.places_nearby(location=(lat, long), radius=radius, open_now=False, type=category,
                                 rank_by=rank_by)
    if result is not None:
        if len(result.get('results')) > 0:
            return result.get('results')
        return None
    else:
        return None
