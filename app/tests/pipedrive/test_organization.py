import pytest
from unittest.mock import MagicMock
from pipedrive.organization import Organization

STANDARD_FIELDS = [
    'id',
    'company_id',
    'owner_id',
    'name',
    'open_deals_count',
    'related_open_deals_count',
    'closed_deals_count',
    'related_closed_deals_count',
    'email_messages_count',
    'people_count',
    'activities_count',
    'done_activities_count',
    'undone_activities_count',
    'reference_activities_count',
    'files_count',
    'notes_count',
    'followers_count',
    'won_deals_count',
    'related_won_deals_count',
    'lost_deals_count',
    'related_lost_deals_count',
    'active_flag',
    'category_id',
    'picture_id',
    'country_code',
    'first_char',
    'update_time',
    'add_time',
    'visible_to',
    'next_activity_date',
    'next_activity_time',
    'next_activity_id',
    'last_activity_id',
    'last_activity_date',
    'address',
    'address_subpremise',
    'address_street_number',
    'address_route',
    'address_sublocality',
    'address_locality',
    'address_admin_area_level_1',
    'address_admin_area_level_2',
    'address_country',
    'address_postal_code',
    'address_formatted_address',
    'owner_name',
    'cc_email',
    'edit_name',
    'last_activity',
    'next_activity',
]


class TestFields:
    def test_returns_active_fields(self):
        org = Organization(auto_load_fields=False)

        name = dict(id=1, key='name', name='Name', active_flag=True)
        xpto = dict(id=2, key='xpto', name='Xpto', active_flag=False)
        address = dict(id=3, key='address', name='Address', active_flag=True)

        fields = [name, xpto, address]
        org._request = MagicMock(return_value=dict(
            data=fields
        ))
        org._load_fields()

        expected_value = [name, address]

        assert list(org.fields()) == expected_value

    def test_returns_all_fields(self):
        org = Organization(auto_load_fields=False)

        name = dict(id=1, key='name', name='Name', active_flag=True)
        xpto = dict(id=2, key='xpto', name='Xpto', active_flag=False)
        address = dict(id=3, key='address', name='Address', active_flag=True)

        fields = [name, xpto, address]
        org._request = MagicMock(return_value=dict(
            data=fields
        ))
        org._load_fields()

        expected_value = fields

        assert list(org.fields(active_only=False)) == expected_value


class TestIsActiveField:
    def test_when_active_returns_true(self):
        org = Organization(auto_load_fields=False)
        field = dict(id=1, key='name', name='Name', active_flag=True)
        org._add_field_to_cache(field)

        assert org.is_active_field(field['key'])

    def test_when_NOT_active_returns_false(self):
        org = Organization(auto_load_fields=False)
        field = dict(id=1, key='name', name='Name', active_flag=False)
        org._add_field_to_cache(field)

        assert not org.is_active_field(field['key'])


class TestFieldName:
    def test_when_standard_field_returns_verbose_name(self):
        org = Organization(auto_load_fields=False)

        field_name = 'This a nice Name'
        field = dict(id=1, key='name', name=field_name, active_flag=False)
        org._add_field_to_cache(field)

        expected_value = field_name
        assert org.field_name('name') == expected_value

    def test_when_hash_field_returns_verbose_name(self):
        org = Organization(auto_load_fields=False)

        field_name = 'This is a test field'
        field = dict(id=1, key='xpto', name=field_name, active_flag=False)
        org._add_field_to_cache(field)

        expected_value = field_name
        assert org.field_name('xpto') == expected_value

    def test_when_field_has_the_same_name_as_a_standard_one_returns_hash(self):
        org = Organization(auto_load_fields=False)

        field_key = '#hashName'
        field = dict(id=1, key='#hashName', name='name', active_flag=False)
        org._add_field_to_cache(field)

        expected_value = field_key
        assert org.field_name(field_key) == expected_value


class TestFieldKey:
    @pytest.mark.parametrize('field', STANDARD_FIELDS)
    def test_when_standard_field_returns_same_name(self, field):
        org = Organization(auto_load_fields=False)

        expected_value = field
        assert org.field_key(field) == expected_value

    def test_when_field_does_no_exists_create_a_new_one(self):
        org = Organization(auto_load_fields=False)

        field_key = '##newField##'
        field_name = 'New Nice Field'
        field = dict(id=1, key=field_key, name=field_name, active_flag=True)

        org._request = MagicMock(return_value=dict(
            data=field
        ))

        expected_value = field_key
        assert org.field_key(field_name) == expected_value

    def test_when_create_a_new_fields_cache_it(self):
        org = Organization(auto_load_fields=False)

        field_key = '##newField##'
        field_name = 'New Nice Field'
        field = dict(id=1, key=field_key, name=field_name, active_flag=True)

        org._request = MagicMock(return_value=dict(
            data=field
        ))

        expected_value = [field]
        org.field_key(field_name)

        assert list(org.fields(active_only=False)) == expected_value


class TestCreate:
    def test_when_creating_organization_skips_fields_not_allowed_on_create(self):  # noqa: E501
        org = Organization(auto_load_fields=False)

        name = dict(
            id=1, key='#name#', name='Name Nice', active_flag=True,
            add_visible_flag=True
        )
        xpto = dict(
            id=2, key='xpto', name='Xpto',  active_flag=True,
            add_visible_flag=False
        )
        address = dict(
            id=3, key='address', name='Address', active_flag=True,
            add_visible_flag=True
        )
        _id = dict(
            id=4, key='id', name='ID',  active_flag=True,
            add_visible_flag=True
        )
        for field in (name, xpto, address, _id):
            org._add_field_to_cache(field)

        org.url = MagicMock(return_value='fake-url')
        org._request = MagicMock(return_value=dict(
            data={'id': 1, '#name#': 'batman is a nice name'}
        ))

        data = {
            'Name Nice': 'batman is a nice name',
            'Xpto': 'this will be skipped :)'
        }
        org.create(data)
        org._request.assert_called_with(
            'POST', 'fake-url', data={'#name#': 'batman is a nice name'}
        )

    def test_when_create_org_returns_detail(self):
        org = Organization(auto_load_fields=False)

        name = dict(
            id=1, key='#name#', name='Name Nice', active_flag=True,
            add_visible_flag=True
        )
        _id = dict(
            id=4, key='id', name='Super ID:',  active_flag=True,
            add_visible_flag=True
        )
        for field in (name, _id):
            org._add_field_to_cache(field)

        org.url = MagicMock(return_value='fake-url')

        org._request = MagicMock(return_value=dict(
            data={'id': 1, '#name#': 'batman is a nice name'}
        ))

        data = {
            'Name Nice': 'batman is a nice name',
        }
        expected_value = {'id': 1, '#name#': 'batman is a nice name'}

        assert org.create(data) == expected_value


class TestDetail:
    def test_returns_active_fields(self):
        org = Organization(auto_load_fields=False)

        name = dict(
            id=1, key='#name#', name='Name Nice', active_flag=True,
            add_visible_flag=True
        )
        _id = dict(
            id=4, key='id', name='Super ID:',  active_flag=False,
            add_visible_flag=True
        )
        for field in (name, _id):
            org._add_field_to_cache(field)

        org._request = MagicMock(return_value=dict(
            data={'id': 1, '#name#': 'batman is a nice name'}
        ))

        expected_value = {'#name#': 'batman is a nice name'}

        assert org.detail(1) == expected_value


class TestSearch:
    def test_when_searching_pass_the_search_key_on_url(self):
        org = Organization(auto_load_fields=False)

        org._request = MagicMock(return_value=dict(data=[]))

        org.ORGANIZATION_SEARCH = 'fake-endpoint'
        org.url = MagicMock()

        search_key = 'XPTO ASD'
        list(org.search(search_key))
        org.url.assert_called_with('fake-endpoint', dict(term=search_key))

    def test_returns_detail_of_organizations_found(self):
        org = Organization(auto_load_fields=False)

        _id = dict(
            id=4, key='id', name='Super ID:',  active_flag=True,
            add_visible_flag=True
        )
        org._add_field_to_cache(_id)

        org._request = MagicMock(return_value=dict(
            data=[{'id': 1}, {'id': 2}, {'id': 3}]
        ))
        org.detail = MagicMock()
        list(org.search(None))
        for _id in (1, 2, 3):
            org.detail.assert_any_call(1)


class TestAll:
    def test_retuns_organizations(self):
        org = Organization(auto_load_fields=False)

        name = dict(
            id=1, key='#name#', name='Name Nice', active_flag=False,
            add_visible_flag=True
        )
        _id = dict(
            id=4, key='id', name='Super ID:',  active_flag=True,
            add_visible_flag=True
        )
        for field in (name, _id):
            org._add_field_to_cache(field)

        org._request = MagicMock(return_value=dict(
            data=[
                {'id': 1, '#name#': 'batman is a nice name'},
                {'id': 2, '#name#': 'superman'},
            ]
        ))

        expected_value = [
            {'id': 1},
            {'id': 2},
        ]

        assert list(org.all()) == expected_value
