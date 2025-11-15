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
    def test_org(
            self,
            org_name: str,
            mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        # 1. ARRANGE: Set up the mock and the client
        
        # We create a sample payload that we expect `get_json` to return
        test_payload = {"name": org_name, "repos_url": "http://some.url"}
        
        # We configure our mock: when `get_json` is called,
        # it must return our sample payload.
        mock_get_json.return_value = test_payload
        
        # Instantiate the class we are testing
        client = GithubOrgClient(org_name)

        # 2. ACT: Call the method we are testing
        result = client.org

        # 3. ASSERT: Check that everything happened as expected
        
        # Check that the result is the payload we told the mock to return
        self.assertEqual(result, test_payload)
        
        # Check that our mock (`get_json`) was called exactly once,
        # and with the correct URL.
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
