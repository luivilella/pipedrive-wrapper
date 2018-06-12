import geopy.distance


def geo_sorted(base_point, list_to_sort, key_func):
    def key(obj):
        distance = geopy.distance.vincenty(base_point, key_func(obj)).km
        return distance
    return sorted(list_to_sort, key=key)
