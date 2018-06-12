from utils.geo_sort import geo_sorted


class TestGeoSorted:
    def test_returns_results_sorted_by_geolocation(self):
        cities = [
            ('IE - Dublin', 53.350140, -6.266155),
            ('BR - Rio de Janeiro', -22.970722, -43.182365),
            ('US - San Francisco', 37.773972, -122.431297),
            ('US - NYC', 40.730610, -73.935242),
            ('BR - Sao Paulo', -23.533773, -46.625290),
        ]

        my_point = (-34.603722, -58.381592)  # AR - Buenos Aires, Argentina

        expected_value = [
            ('BR - Sao Paulo', -23.533773, -46.62529),
            ('BR - Rio de Janeiro', -22.970722, -43.182365),
            ('US - NYC', 40.73061, -73.935242),
            ('US - San Francisco', 37.773972, -122.431297),
            ('IE - Dublin', 53.35014, -6.266155)
        ]

        lat_lng = slice(1, 3)
        result = geo_sorted(my_point, cities, lambda row: row[lat_lng])
        assert result == expected_value
