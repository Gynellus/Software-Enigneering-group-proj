import unittest
from unittest.mock import patch
from utils import convert_input_to_string, translate_to_dutch, summarize, process_paper_data


class TestConvertInputToString(unittest.TestCase):

    def test_convert_pdf_file(self):
        # Test with a mock PDF file path
        result = convert_input_to_string('mock_file.pdf')
        self.assertIsInstance(result, str)
        # Add more assertions based on the expected output

    def test_convert_url(self):
        # Test with a mock URL
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b'Mock content'
            result = convert_input_to_string('http://mockurl.com')
            self.assertIsInstance(result, str)
            # Add more assertions based on the expected output

    def test_convert_plain_text(self):
        # Test with plain text
        result = convert_input_to_string('This is a test string.')
        self.assertEqual(result, 'This is a test string.')

    def test_unsupported_format(self):
        # Test with unsupported input
        result = convert_input_to_string(None)
        self.assertEqual(result, 'Unsupported data format')


# Add more test cases as needed
class TestProcessPaperData(unittest.TestCase):

    @patch('utils.summarize_similar_papers')
    @patch('utils.find_similar_papers')
    def test_process_paper_data(self, mock_find, mock_summarize):
        mock_find.return_value = [{'url': 'mock_url', 'title': 'mock_title'}]
        mock_summarize.return_value = [{'url': 'mock_url', 'title': 'mock_title', 'summary': 'mock_summary'}]

        result = process_paper_data('Some paper text')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn('summary', result[0])


class TestSummarize(unittest.TestCase):

    @patch('utils.OpenAI')
    def test_summarize(self, mock_openai):
        # Setup the mock to return a Mock object with the required attributes
        mock_choice = unittest.mock.MagicMock()
        mock_choice.message.content = 'Mock summary'
        mock_openai.return_value.chat.completions.create.return_value.choices = [mock_choice]

        # Call your summarize function
        result = summarize('Mock article text')

        # Assertions
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'Mock summary\n\n')

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            summarize('')


class TestTranslateToDutch(unittest.TestCase):

    @patch('utils.OpenAI')
    def test_translate_to_dutch(self, mock_openai):
        # Mock the API response structure
        mock_response = unittest.mock.MagicMock()
        mock_choice = unittest.mock.MagicMock()
        mock_choice.message.content = '[[Vertaald]]'
        mock_response.choices = [mock_choice]
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        # Call your translate_to_dutch function
        result = translate_to_dutch('Some text to translate')

        # Print the result for debugging
        print("Translated text:", result)
        # Assertions
        expected_translation = 'Vertaal'
        # Process and extract the actual translation
        translated_text = result[result.find("[[") + 2:result.find("]]")]

        self.assertEqual(translated_text, expected_translation)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            print(translate_to_dutch(''))


if __name__ == '__main__':
    unittest.main()