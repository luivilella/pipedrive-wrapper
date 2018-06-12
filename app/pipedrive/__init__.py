from .organization import Organization


class PipeDrive:
    def __init__(self, api_key=None, api_url=None):
        self.organization = Organization(api_key, api_url)
