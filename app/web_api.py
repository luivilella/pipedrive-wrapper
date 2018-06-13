from bottle import Bottle, request, response
from environs import Env

from services.pipedrive_organization import PipeDriveOrganizationService
from utils.ip_info import get_ip_info

env = Env()
GEOLOCATION_BACKEND_SORT = env.bool('GEOLOCATION_BACKEND_SORT', False)
HTTP_REMOTE_ADDR = env('HTTP_REMOTE_ADDR', 'REMOTE_ADDR')


service = PipeDriveOrganizationService()
app = Bottle()


@app.route('/organizations', method='GET')
def search():
    search = request.GET.get('search', '').strip()
    getsort = request.GET.get('getsort', '').strip()
    geolocation_sort = None
    if getsort:
        lat, lng = getsort.split(',')
        geolocation_sort = (float(lat), float(lng))

    if not geolocation_sort and GEOLOCATION_BACKEND_SORT:
        ip_info = get_ip_info(request.environ.get(HTTP_REMOTE_ADDR))
        lat, lng = ip_info.get('lat'), ip_info.get('lon')
        if lat is not None and lng is not None:
            geolocation_sort = (lat, lng)
    try:
        organizations = list(
            service.search(search, geolocation_sort)
        )
    except ConnectionError as e:
        response.status = 400
        return dict(success=False, error=str(e))

    return dict(success=True, data=organizations)


@app.route('/organizations', method='POST')
def create():
    json_data = request.json
    post_data, field_type = json_data['data'], json_data.get('field_type', {})

    data = {}
    for field, value in post_data.items():
        data[field] = value
        if field_type.get(field) == 'address':
            data[field] = f'{value["lat"]},{value["lng"]}'

    try:
        organization = service.create(data, field_type)
    except ConnectionError as e:
        response.status = 400
        return dict(success=False, error=str(e))

    return dict(success=True, data=organization)


@app.route('/organizations/<organization_id:int>', method='GET')
def detail(organization_id):
    try:
        organization = service.detail(organization_id)
        fields = list(service.fields())
    except ConnectionError as e:
        response.status = 400
        return dict(success=False, error=str(e))

    return dict(
        success=True,
        data=dict(data=organization, fields=fields)
    )


@app.route('/organizations-fields', method='GET')
def fields():
    try:
        fields = list(service.fields())
    except ConnectionError as e:
        response.status = 400
        return dict(success=False, error=str(e))

    return dict(success=True, data=fields)
