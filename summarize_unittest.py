# Import necessary libraries for unit testing
import unittest
from unittest.mock import patch, MagicMock
import summarize  # Import the module containing the function under test

# This class mocks the OpenAI API's response to simulate actual API calls in the tests.
class MockCompletion:
    def __init__(self, content):
        # Create a mock completion response with a specified content.
        self.choices = [MagicMock(message=MagicMock(content=content))]

# The unit test suite for the summarize function.
class TestSummarize(unittest.TestCase):

    # Tests the summarize function with typical input.
    @patch('summarize.openai')
    def test_summarize_with_normal_input(self, mock_openai):
        # Arrange: Set up the test with expected input and output.
        text = "This is a test article to be summarized."
        expected_summary = "This is a summary."
        # Configure the mock to return a predetermined summary.
        mock_openai.chat.completions.create.return_value = MockCompletion(expected_summary)

        # Act: Call the summarize function with the test input.
        summary = summarize.summarize(text)

        # Assert: Check if the function's output matches the expected output.
        self.assertEqual(summary, expected_summary + "\n\n")
        # Verify that the OpenAI API's create function was indeed called.
        mock_openai.chat.completions.create.assert_called()

    # Tests the summarize function with empty input to ensure it raises a ValueError.
    @patch('summarize.openai')
    def test_summarize_with_empty_input(self, mock_openai):
        # Arrange: Prepare an empty string as input.
        text = ""

        # Act & Assert: Expect a ValueError when summarize is called with empty input.
        with self.assertRaises(ValueError):
            summarize.summarize(text)

    # Tests the summarize function with input longer than the typical use case.
    @patch('summarize.openai')
    def test_summarize_with_very_long_input(self, mock_openai):
        # Arrange: Create a string longer than the expected input size limit.
        text = "a" * 10001  # A very long text
        expected_summary = "This is a summary of the very long text."
        # Configure the mock to return a predetermined summary for the long text.
        mock_openai.chat.completions.create.return_value = MockCompletion(expected_summary)

        # Act: Call the summarize function with the test input.
        summary = summarize.summarize(text)

        # Assert: Check if the function's output includes the expected summary.
        self.assertIn(expected_summary, summary)
        # Verify that the OpenAI API's create function was called.
        mock_openai.chat.completions.create.assert_called()

    # Tests the summarize function with input that contains special characters.
    @patch('summarize.openai')
    def test_summarize_with_special_characters(self, mock_openai):
        # Arrange: Set up the test input with a variety of special characters.
        text = "!@#$%^&*()_+{}|:\"<>?`~"
        expected_summary = "This is a summary with special characters."
        # Configure the mock to return a predetermined summary that includes special characters.
        mock_openai.chat.completions.create.return_value = MockCompletion(expected_summary)

        # Act: Call the summarize function with the test input.
        summary = summarize.summarize(text)

        # Assert: Check if the function's output matches the expected output.
        self.assertEqual(summary, expected_summary + "\n\n")
        # Verify that the OpenAI API's create function was called.
        mock_openai.chat.completions.create.assert_called()

# The standard boilerplate to run the test suite if the script is executed directly.
if __name__ == '__main__':
    unittest.main()
