#!/usr/bin/env python3
"""Fixtures for testing client"""

org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1"},
    {"id": 2, "name": "repo2"}
]

expected_repos = ["repo1", "repo2"]

org_payload_with_license = [
    {"name": "repo1", "license": {"key": "mit"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
    {"name": "repo3"}
]
