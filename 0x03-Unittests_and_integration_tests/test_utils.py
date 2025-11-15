#!/usr/bin/env python3
"""
Unit test for utils.py
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, get_json
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                                 nested_map: Mapping,
                                 path: Sequence,
                                 expected: Any) -> None:
        """
        Test that access_nested_map returns the correct value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping,
                                         path: Sequence,
                                         expected_message: str) -> None:
        """
        Test that KeyError is raised for invalid paths and
        that the exception message is correct.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        self.assertEqual(str(cm.exception), f"'{expected_message}'")


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self,
                      test_url: str,
                      test_payload: dict) -> None:
        """
        Test that get_json returns the expected payload
        by mocking the external HTTP call.
        """
        with patch('utils.requests.get') as mock_get:
            
            mock_response = mock_get.return_value
            mock_response.json.return_value = test_payload

            result = get_json(test_url)

            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)