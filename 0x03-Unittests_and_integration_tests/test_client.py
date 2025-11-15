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
        # 1. ARRANGE: Define the known payload 'org' should return
        known_payload = {"repos_url": "https://api.github.com/my_test/repos"}

        # 2. ARRANGE & ACT: Patch 'org' as a property
        # We patch 'org' on the GithubOrgClient class
        # 'new_callable=PropertyMock' is the key. It tells patch
        # to create a mock that *acts like a property*, not a method.
        with patch.object(GithubOrgClient,
                          'org',
                          new_callable=PropertyMock) as mock_org:

            # Configure the mock property to return our payload
            mock_org.return_value = known_payload

            # Instantiate the client
            client = GithubOrgClient("test_org")

            # Call the property we are testing.
            # This will internally call the mocked 'client.org'
            result = client._public_repos_url

        # 3. ASSERT: Check that the result is what we expect
        self.assertEqual(result, known_payload["repos_url"])
