#!/usr/bin/env python3
"""
Unit test for utils.py
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any, Dict


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
                      test_payload: Dict) -> None:
        """
        Test that get_json returns the expected payload
        by mocking the external HTTP call.
        """
        # We need to create a Mock object for the response
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        with patch('utils.requests.get', return_value=mock_response) as mock_get:

            result = get_json(test_url)

            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Test class for the memoize decorator.
    """
    def test_memoize(self) -> None:
        """
        Test that memoize caches the result of a method
        and the underlying method is only called once.
        """
        class TestClass:
            def a_method(self) -> int:
                """A simple method."""
                return 42

            @memoize
            def a_property(self) -> int:
                """A memoized property."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            
            mock_a_method.return_value = 42

            test_instance = TestClass()

            result_1 = test_instance.a_property
            result_2 = test_instance.a_property

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)

            mock_a_method.assert_called_once()