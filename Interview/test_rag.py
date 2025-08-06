
import unittest
from unittest.mock import patch, MagicMock
import os
import fitz  # PyMuPDF
from rag import get_pdf_text, recursive_character_text_splitter

class TestRAG(unittest.TestCase):

    def setUp(self):
        """Set up a dummy PDF for testing."""
        self.pdf_path = "test.pdf"
        doc = fitz.open()  # Create a new PDF
        page = doc.new_page()
        page.insert_text((72, 72), "This is a test document.")
        doc.save(self.pdf_path)
        doc.close()

    def tearDown(self):
        """Remove the dummy PDF after testing."""
        os.remove(self.pdf_path)

    def test_get_pdf_text(self):
        """Test that the PDF text is extracted correctly."""
        text = get_pdf_text(self.pdf_path)
        self.assertEqual(text, "This is a test document.")

    def test_recursive_character_text_splitter(self):
        """Test that the text is split correctly."""
        text = "This is a long text that needs to be split into smaller chunks."
        chunks = recursive_character_text_splitter(text, 20, 5)
        self.assertEqual(len(chunks), 5)
        self.assertEqual(chunks[0], "This is a long text ")
        self.assertEqual(chunks[1], "long text that needs")

    @patch('rag.OpenAI')
    def test_main_flow(self, MockOpenAI):
        """Test the main RAG pipeline with mocked OpenAI calls."""
        # Mock the OpenAI client and its methods
        mock_client = MagicMock()
        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
        )
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="This is a test response."))]
        )
        MockOpenAI.return_value = mock_client

        # Mock the input function
        with patch('builtins.input', return_value='What is this document about?'):
            # We need to import main from rag inside the test function to use the mocked OpenAI
            from rag import main
            # We need to redirect stdout to capture the output
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()

            main()
            # We just check that the function runs without errors
            pass

if __name__ == '__main__':
    unittest.main()
