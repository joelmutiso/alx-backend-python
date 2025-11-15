# ALX Backend Python: 0x03. Unittests and Integration Tests

## 📋 Project Overview

This project is the next step in our ALX backend specialization, moving from just *writing* code to *proving* our code works.

As a full-stack developer, especially when building projects like your **AirBnB clone** or the **Django travel app**, you need a way to guarantee that your logic is solid. This project introduces the tools and techniques to do just that: unit and integration testing.

We will learn to use Python's built-in `unittest` library to test our functions in isolation (unit tests) and then test how they work together with external systems (integration tests).

## 🎓 Learning Objectives

This project will build on your Python knowledge (like decorators and generators) and teach you the critical skills of a professional developer:

* Explain the difference between unit and integration tests.
* Write unit tests for Python code using the `unittest` framework.
* Implement common testing patterns, including:
    * **Mocking:** How to "fake" external calls (like GitHub APIs) to test your function's logic in isolation.
    * **Parameterization:** A clean way to run the same test with many different inputs.
    * **Fixtures:** Using pre-defined data (like `fixtures.py`) to get consistent test results.

## 🚀 Why This Matters for Your Goals

* **For your Django Projects (`alx_travel_app`):** Unit tests are perfect for testing a single function in your `views.py` or a method on your models.
* **For your AirBnB Clone:** Integration tests will be how you verify that a user can *actually* sign up, log in, and book a room—a test that spans your views, models, and database all at once.
* **For Professional Development:** Writing tests is a non-negotiable skill in any software engineering role. It's how you build reliable, maintainable applications.

## 📂 Files

* `utils.py`: Contains utility functions (like `access_nested_map`) that we will be testing.
* `client.py`: A `GithubOrgClient` class that we will test.
* `fixtures.py`: Pre-made data to use in our tests, ensuring consistent results.
* `test_utils.py`: Our unit tests for `utils.py`.
* `test_client.py`: Our unit and integration tests for `client.py`.

## ⚙️ How to Run Tests

All tests are run from the command line using Python's `unittest` module:

```bash
python3 -m unittest path/to/test_file.py