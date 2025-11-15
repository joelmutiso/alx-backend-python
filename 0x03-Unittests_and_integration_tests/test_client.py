#!/usr/bin/env python3
"""
Unit test for client.py
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for the GithubOrgClient.
    """
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
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
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test public_repos by mocking _public_repos_url and get_json.
        """
        # ARRANGE
        test_repos_payload = [
            {"name": "repo-one"},
            {"name": "repo-two"}
        ]
        expected_repos = ["repo-one", "repo-two"]

        mock_get_json.return_value = test_repos_payload

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:

            fake_url = "https://fake.url/repos"
            mock_public_repos_url.return_value = fake_url

            # ACT
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            # ASSERT
            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self,
                           repo: Dict,
                           license_key: str,
                           expected: bool) -> None:
        """
        Test the has_license static method with parameterized inputs.
        """
        # ACT
        result = GithubOrgClient.has_license(repo, license_key)

        # ASSERT
        self.assertEqual(result, expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [(org_payload, repos_payload, expected_repos, apache2_repos)])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.
    Mocks external HTTP calls using class-level fixtures.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by patching requests.get.
        This method is called ONCE before any tests run.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """
            Returns a mock response based on the URL.
            """
            if url.endswith("/orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class by stopping the patcher.
        This method is called ONCE after all tests run.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos returns all repos correctly.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos filters repos by license correctly.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


