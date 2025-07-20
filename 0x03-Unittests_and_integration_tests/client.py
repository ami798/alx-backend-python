#!/usr/bin/env python3
"""Client module to interface with GitHub API."""

from typing import Dict, List
from utils import get_json, memoize


class GithubOrgClient:
    """GitHub Organization Client."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize with org name."""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization data."""
        url = self.ORG_URL.format(org=self._org_name)
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """Get the URL to the list of public repos."""
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """List public repositories."""
        repos_data = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos_data]
        if license:
            repo_names = [repo["name"] for repo in repos_data
                          if repo.get("license", {}).get("key") == license]
        return repo_names

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key
