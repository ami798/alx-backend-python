#!/usr/bin/env python3
"""Test suite for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class

from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    org_payload_with_license
)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": ["repo2"]}
])
class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get"""
        cls.get_patcher = patch('client.get_json', side_effect=[
            cls.org_payload, cls.repos_payload
        ])
        cls.mock_get_json = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Unpatch requests.get"""
        cls.get_patcher.stop()

    def test_org(self):
        """Test org property"""
        client = GithubOrgClient("google")
        self.assertEqual(client.org, self.org_payload)

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = self.org_payload
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                self.org_payload["repos_url"]
            )

    def test_public_repos(self):
        """Test public_repos method"""
        with patch('client.get_json', return_value=self.repos_payload):
            with patch.object(GithubOrgClient, '_public_repos_url',
                              new_callable=PropertyMock) as mock_repos_url:
                mock_repos_url.return_value = self.org_payload["repos_url"]
                client = GithubOrgClient("google")
                self.assertEqual(client.public_repos(), self.expected_repos)

    def test_has_license(self):
        """Test has_license method"""
        client = GithubOrgClient("google")
        repo = {"license": {"key": "apache-2.0"}}
        self.assertTrue(client.has_license(repo, "apache-2.0"))
