from geopy.distance import geodesic


def geo_sorted(base_point, list_to_sort, key_func):
    def key(obj):
        distance = geodesic(base_point, key_func(obj)).km
        return distance
    return sorted(list_to_sort, key=key)
