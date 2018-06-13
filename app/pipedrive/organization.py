from .base import PDBase
from .conf import (
    ORGANIZATION,
    ORGANIZATION_DETAIL,
    ORGANIZATION_FIELDS,
    ORGANIZATION_SEARCH,
    ORGANIZATION_STANDARD_FIELDS,
)


class Organization(PDBase):
    ORGANIZATION = ORGANIZATION
    ORGANIZATION_DETAIL = ORGANIZATION_DETAIL
    ORGANIZATION_FIELDS = ORGANIZATION_FIELDS
    ORGANIZATION_SEARCH = ORGANIZATION_SEARCH
    STANDARD_FIELDS = ORGANIZATION_STANDARD_FIELDS

    def __init__(self, api_key=None, api_url=None, auto_load_fields=True):
        super().__init__(api_key, api_url)
        self._active_fields = set()
        self._cache_fields_name = {}
        self._cache_fields_key = {}
        self._fields = []
        if auto_load_fields:
            self._load_fields()

    def _add_field_to_cache(self, field):
        self._cache_fields_key[field['key']] = field
        self._cache_fields_name[field['name']] = field
        self._fields.append(field)

        if field['active_flag']:
            self._active_fields.add(field['id'])

    def fields(self, active_only=True):
        for field in self._fields:
            if active_only and not self.is_active_field(field['key']):
                continue
            yield field.copy()

    def _load_fields(self):
        url = self.url(self.ORGANIZATION_FIELDS)
        fields = self._request('GET', url)['data'] or []
        for field in fields:
            self._add_field_to_cache(field)

    def is_active_field(self, field_key):
        field = self._cache_fields_key.get(field_key, {})
        return field.get('id') in self._active_fields

    def _detail_to_dict(self, detail, active_only=True):
        if active_only:
            return {
                field_key: value for field_key, value in detail.items()
                if self.is_active_field(field_key)
            }
        return detail

    def field_name(self, field_name):
        if field_name in self.STANDARD_FIELDS:
            return field_name

        field = self._cache_fields_key.get(field_name, {})
        name = field.get('name', field_name)
        if name in self.STANDARD_FIELDS:
            return field_name
        return name

    def field_key(self, field_name, field_type=None):
        if field_name in self.STANDARD_FIELDS:
            return field_name

        field = self._cache_fields_name.get(field_name)
        if not field:
            url = self.url(self.ORGANIZATION_FIELDS)
            field = self._request(
                'POST',
                url,
                data=dict(
                    name=field_name,
                    field_type=field_type or 'varchar_auto',
                )
            )['data']
            self._add_field_to_cache(field)

        return field['key']

    def field_allowed_on_create(self, field_key):
        field = self._cache_fields_key[field_key]
        return bool(field.get('add_visible_flag'))

    def create(self, data, field_type=None):
        field_type = field_type or {}
        post_data = {}
        for field_name, value in data.items():
            field_key = self.field_key(field_name, field_type.get(field_name))
            if not self.field_allowed_on_create(field_key):
                continue
            post_data[field_key] = value

        url = self.url(self.ORGANIZATION)
        detail = self._request('POST', url, data=post_data)['data']
        return self._detail_to_dict(detail)

    def detail(self, organization_id):
        url = self.url(self.ORGANIZATION_DETAIL.format(organization_id))
        detail = self._request('GET', url)['data'] or {}
        return self._detail_to_dict(detail)

    def search(self, search_key):
        url = self.url(self.ORGANIZATION_SEARCH, dict(term=search_key))
        search_results = self._request('GET', url)
        for result in search_results['data'] or []:
            organization = self.detail(result['id'])
            yield organization

    def all(self):
        url = self.url(self.ORGANIZATION)
        organizations = self._request('GET', url)['data'] or []
        for detail in organizations:
            yield self._detail_to_dict(detail)
