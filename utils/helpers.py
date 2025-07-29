"""
Helper functions for the Synthetic Data Generator
"""

import gradio as gr
from config.settings import file_format_options
from generators.data_generator import SyntheticDataGenerator

# Initialize the generator
generator = SyntheticDataGenerator()

def update_options(file_format):
    """Update dropdown options based on file format selection"""
    if file_format in file_format_options:
        config = file_format_options[file_format]
        return (
            gr.Dropdown(choices=config["size_options"], label=config["size_label"], value=config["size_options"]),
            gr.Dropdown(choices=config["content_options"], label=config["content_label"], value=config["content_options"])
        )
    return gr.Dropdown(choices=[], label="Size"), gr.Dropdown(choices=[], label="Content Type")

def generate_synthetic_data(file_format, size_value, content_value, subject_input):
    """Main function to generate synthetic data based on selections and subject"""
    try:
        # Use default subject if empty
        subject = subject_input.strip() if subject_input.strip() else "general topics"
        
        if file_format in ["Word Document (.docx)", "PDF Document (.pdf)", "Text File (.txt)"]:
            # Generate document content with subject
            pages = int(size_value)
            content_type = content_value
            
            return generator.generate_document(content_type, pages, subject, file_format)
            
        elif file_format in ["Excel Spreadsheet (.xlsx)", "CSV File (.csv)"]:
            # Generate Excel/CSV data with subject context
            rows = int(size_value)
            columns = int(content_value)
            
            return generator.generate_data_file(rows, columns, subject, file_format)
        
        else:
            # Handle unexpected file format
            return None, f"❌ Error: Unsupported file format: {file_format}"
            
    except Exception as e:
        # Make sure we ALWAYS return exactly 2 values
        error_msg = f"❌ Error: {str(e)}"
        print(f"Exception in generate_synthetic_data: {error_msg}")  # Debug print
        return None, error_msg
