from environs import Env


env = Env()

PIPEDRIVE_URL = env(
    'PIPEDRIVE_URL', 'https://api.pipedrive.com/v1/'
)

PIPEDRIVE_API_KEY = env('PIPEDRIVE_API_KEY', '123change')

SEARCH_URL = 'searchResults'

ORGANIZATION = 'organizations'
ORGANIZATION_DETAIL = 'organizations/{}'
ORGANIZATION_FIELDS = 'organizationFields'
ORGANIZATION_SEARCH = 'organizations/find'

ORGANIZATION_STANDARD_FIELDS = {
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
}
