from itertools import chain
from pipedrive import PipeDrive
from utils.geo_sort import geo_sorted


class PipeDriveOrganizationService:
    def __init__(self):
        self.pd = PipeDrive()

    def search(self, search, geolocation_sort=None):
        if search:
            organizations = self.pd.organization.search(search)
        else:
            organizations = self.pd.organization.all()

        if not geolocation_sort:
            return organizations

        def valid_lat_long(organization):
            address = organization.get('address') or ''
            params = address.split(',')
            if len(params) == 2 and all(params):
                return True
            return False

        def invalid_lat_lng(organization):
            return not valid_lat_long(organization)

        def get_lat_lng(obj):
            latitude, longitude = obj['address'].split(',')
            return (float(latitude), float(longitude))

        organizations_sorted_by_lat_lng = geo_sorted(
            geolocation_sort,
            filter(valid_lat_long, organizations),
            get_lat_lng
        )

        return chain(
            organizations_sorted_by_lat_lng,
            filter(invalid_lat_lng, organizations)
        )

    def detail(self, organization_id):
        return self.pd.organization.detail(organization_id)

    def create(self, data, field_type=None):
        return self.pd.organization.create(data, field_type)

    def fields(self):
        return self.pd.organization.fields()
