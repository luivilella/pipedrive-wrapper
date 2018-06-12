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

        organizations_filtered = filter(
            lambda obj: obj.get('address'), organizations
        )

        def get_lat_lng(obj):
            latitude, longitude = obj['address'].split(',')
            return (float(latitude), float(longitude))
        organizations_sorted = geo_sorted(
            geolocation_sort, organizations_filtered, get_lat_lng
        )

        return organizations_sorted

    def detail(self, organization_id):
        return self.pd.organization.detail(organization_id)

    def create(self, data, field_type=None):
        return self.pd.organization.create(data, field_type)

    def fields(self):
        return self.pd.organization.fields()
