import requests
import tempfile
from openai import OpenAI
import os
from .document_generator import DocumentGenerator
from .excel_generator import ExcelGenerator

class SyntheticDataGenerator:
    def __init__(self, use_llama4=False):
        # Set this variable to True for llama4.cc-demos.com, False for Ollama
        self.use_llama4 = use_llama4

        if self.use_llama4:
            self.api_base_url = "https://llama4.cc-demos.com/v1"
            self.api_key = "openai"  # Use proper key if needed
        else:
            self.api_base_url = "http://localhost:11434/api/generate"
            self.api_key = None  # Ollama usually doesn't require an API key

        self.document_generator = DocumentGenerator(self)
        self.excel_generator = ExcelGenerator(self)
        self.client = OpenAI(
            base_url=self.api_base_url,
            api_key=self.api_key,
        )

    def generate_with_ollama(self, prompt, max_tokens=None):
        """Generate content via Llama 4 Chat API (Ollama or llama4.cc-demos.com)."""
        try:
            messages = [
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model="meta/llama-4-scout-17b-16e-instruct",  # Replace if needed
                messages=messages,
                temperature=0.7,
                top_p=0.9,
                max_tokens=max_tokens or 4000,
            )
            return response.choices.message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_document(self, content_type, pages, subject, file_format):
        """Generate document content and create file"""
        return self.document_generator.generate_document(content_type, pages, subject, file_format)

    def generate_data_file(self, rows, columns, subject, file_format):
        """Generate Excel/CSV data file"""
        return self.excel_generator.generate_data_file(rows, columns, subject, file_format)
