import googlemaps

gmaps = googlemaps.Client(key='')


def nearby_places(lat, long, category, radius=None):
    rank_by = 'distance'

    # TODO: open_now should be set to True in a production environment,
    #       for testing purposes during COVID19 we set it to False

    result = gmaps.places_nearby(location=(lat, long), radius=radius, open_now=False, type=category,
                                 rank_by=rank_by)
    if result is not None:
        if len(result.get('results')) > 0:
            return result.get('results')
        return None
    else:
        return None
