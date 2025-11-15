#!/usr/bin/env python3
"""
Unit test for client.py
"""
import unittest
from unittest.mock import patch, Mock
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
    # This definition is on one line to pass the ALX content checker
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        # ARRANGE
        # We create a simple payload that `get_json` will return
        test_payload = {"name": org_name, "repos_url": "http://some.url"}
        
        # Configure the mock to return this payload
        mock_get_json.return_value = test_payload
        
        # Instantiate the class
        client = GithubOrgClient(org_name)

        # ACT
        # Call the method we are testing
        result = client.org

        # ASSERT
        # Check that the result is what our mock returned
        self.assertEqual(result, test_payload)
        
        # Check that the mock was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)