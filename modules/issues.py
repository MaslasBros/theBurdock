import requests
from abc import ABC, abstractmethod

class RestAPI(ABC):
    """
    Abstract base class (interface) for REST API clients.
    Provides a base session and defines generic REST operations.
    """

    def __init__(self, base_url: str, headers: dict, api_key: str):
        """
        Initialize the API client.

        :param base_url: Base URL of the REST API
        :param headers: Dictionary of HTTP headers
        :param api_key: API key or token (usage defined by subclass)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update(headers)

    @abstractmethod
    def get(self, endpoint: str, params: dict = None):
        """Perform a GET request to a given endpoint."""
        pass

    @abstractmethod
    def post(self, endpoint: str, data: dict = None):
        """Perform a POST request to a given endpoint."""
        pass
    
    @abstractmethod
    def get_last_issue(self, project_identifier: str):
        """Returns the last issue from the API"""
        pass
    
    @abstractmethod
    def get_last_issues(self, issue_number: int, project_identifier: str):
        """Returns the last issues from the API"""
        pass
