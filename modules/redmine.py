from .issues import RestAPI

class RedmineAPI(RestAPI):
    """
    Redmine REST API client.
    Implements the RestAPI interface for Redmine-specific behavior.
    Docs: https://www.redmine.org/projects/redmine/wiki/Rest_Issues
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Redmine API client with Redmine-specific headers.
        """
        headers = {
            "Content-Type": "application/json",
            "X-Redmine-API-Key": api_key
        }
        super().__init__(base_url, headers, api_key)

    def get(self, endpoint: str, params: dict = None):
        """Generic GET implementation."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"GET {url} failed: {response.status_code} - {response.text}")

        return response.json()

    def post(self, endpoint: str, data: dict = None):
        """Generic POST implementation."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data)

        if response.status_code not in (200, 201):
            raise Exception(f"POST {url} failed: {response.status_code} - {response.text}")

        return response.json()

    def get_last_issue(self, project_identifier: str):
        """
        Fetch the most recent issue from a specified Redmine project.

        :param project_identifier: The project identifier (e.g., "redmine")
        :return: JSON object representing the last issue, or None if not found
        """
        params = {
            "project_id": project_identifier,
            "sort": "created_on:desc",
            "limit": 1
        }

        data = self.get("issues.json", params=params)
        issues = data.get("issues", [])
        return issues[0] if issues else None
    
    def get_last_issues(self, issue_number: int, project_identifier: str):
        """
        Fetch all issues from the specified project with an ID greater than the provided issue_number.

        :param issue_number: The issue number to compare against
        :param project_identifier: The project identifier to filter issues
        :return: List of issues with ID greater than issue_number in the project
        """
        issues = []
        offset = 0
        limit = 100  # Redmine max limit per request

        while True:
            params = {
                "project_id": project_identifier,
                "sort": "id:asc",
                "limit": limit,
                "offset": offset,
                "status_id": "*",  # Include all statuses
            }

            data = self.get("issues.json", params=params)
            batch = data.get("issues", [])

            # Filter issues with id > issue_number locally
            filtered_batch = [issue for issue in batch if issue.get("id", 0) > issue_number]

            if not filtered_batch:
                # No more new issues beyond issue_number in this batch
                break

            issues.extend(filtered_batch)

            if len(batch) < limit:
                # No more issues left to fetch
                break

            offset += limit

        return issues

