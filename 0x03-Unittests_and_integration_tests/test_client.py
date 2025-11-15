#!/usr/bin/env python3
"""
Unit test for client.py
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for the GithubOrgClient.
    """
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(
            self,
            org_name: str,
            mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        # ARRANGE
        test_payload = {"name": org_name, "repos_url": "http://some.url"}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)

        # ACT
        result = client.org

        # ASSERT
        self.assertEqual(result, test_payload)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """
        Test the _public_repos_url property by mocking the 'org' property.
        """
        # ARRANGE
        known_payload = {"repos_url": "https://api.github.com/my_test/repos"}

        # ARRANGE & ACT
        with patch.object(GithubOrgClient,
                          'org',
                          new_callable=PropertyMock) as mock_org:
            
            mock_org.return_value = known_payload
            client = GithubOrgClient("test_org")
            result = client._public_repos_url

        # ASSERT
        self.assertEqual(result, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(
            self,
            mock_get_json: Mock) -> None:
        """
        Test public_repos by mocking _public_repos_url and get_json.
        """
        # 1. ARRANGE: Define our payloads
        
        # This is the fake JSON payload (list of repos)
        # that `get_json` will return.
        test_repos_payload = [
            {"name": "repo-one", "license": {"key": "mit"}},
            {"name": "repo-two", "license": {"key": "apache"}}
        ]
        
        # This is the list of names we expect our method to return.
        expected_repos = ["repo-one", "repo-two"]

        # 2. ARRANGE: Configure the mock from the decorator
        # Tell our mocked `get_json` to return the fake payload.
        mock_get_json.return_value = test_repos_payload

        # 3. ARRANGE (Context Manager): Patch the property
        # We also need to mock `_public_repos_url` because
        # it's called by `repos_payload` (which `public_repos` calls).
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:

            # Configure this mock to return a fake URL.
            fake_url = "https://fake.url/repos"
            mock_public_repos_url.return_value = fake_url

            # 4. ACT: Instantiate and call the method
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            # 5. ASSERT
            # Check if the list of repo names is correct.
            self.assertEqual(result, expected_repos)

            # Check that our mocked property was called exactly ONCE.
            mock_public_repos_url.assert_called_once()
            
            # Check that `get_json` was called exactly ONCE
            # with the fake URL from our property mock.
            mock_get_json.assert_called_once_with(fake_url)