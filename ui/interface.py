"""
Gradio User Interface for the Synthetic Data Generator
"""

import gradio as gr
from config.settings import file_format_options, REPORTLAB_AVAILABLE
from utils.helpers import update_options, generate_synthetic_data

def create_gradio_app():
    """Create and configure the Gradio interface"""
    
    with gr.Blocks(title="Synthetic Data Generator", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🎯 Synthetic Data Generator")
        gr.Markdown("Generate synthetic documents and datasets using **local Ollama Mistral model** with enhanced iterative generation for longer documents")
        
        with gr.Row():
            with gr.Column(scale=1):
                # File format selection
                file_format = gr.Dropdown(
                    choices=list(file_format_options.keys()),
                    label="📁 File Format",
                    value="Word Document (.docx)"
                )
                
                # Subject input field
                subject_input = gr.Textbox(
                    label="🎯 Subject/Topic",
                    placeholder="e.g., artificial intelligence, data protection, renewable energy, healthcare technology...",
                    value="artificial intelligence",
                    info="Enter the main topic or subject for your synthetic data"
                )
                
                # Dynamic size options
                size_dropdown = gr.Dropdown(
                    choices=file_format_options["Word Document (.docx)"]["size_options"],
                    label="📏 Number of Pages",
                    value="4"
                )
                
                # Dynamic content type options
                content_dropdown = gr.Dropdown(
                    choices=file_format_options["Word Document (.docx)"]["content_options"],
                    label="📝 Document Type",
                    value="whitepaper"
                )
                
                # Generate button
                generate_btn = gr.Button("🚀 Generate Synthetic Data", variant="primary", size="lg")
                
            with gr.Column(scale=1):
                # Output file and status
                output_file = gr.File(label="📄 Generated File")
                status_text = gr.Textbox(label="📊 Status", interactive=False)
        
        # Event handlers
        file_format.change(
            fn=update_options,
            inputs=[file_format],
            outputs=[size_dropdown, content_dropdown]
        )
        
        generate_btn.click(
            fn=generate_synthetic_data,
            inputs=[file_format, size_dropdown, content_dropdown, subject_input],
            outputs=[output_file, status_text]
        )
        
        # Updated instructions
        gr.Markdown(f"""
        ## 📋 Instructions
        - **🎯 Subject/Topic**: Enter the main subject you want the synthetic data to focus on
        - **📁 File Format**: Choose between Word documents, text files, Excel spreadsheets, or CSV files
        - **🔄 Dynamic Options**: Size and content options change based on your file format selection
        - **📝 Documents**: Select pages (1-50) and document type (whitepaper, article, report, proposal, design)
        - **📊 Excel/CSV**: Select number of rows and columns for tabular data
        - **⚙️ Requirements**: Ensure Ollama is running locally with Mistral model loaded
        
        ## 🚀 Enhanced Features
        - **📄 Iterative Generation**: Documents with 3+ pages use section-by-section generation for better length consistency
        - **📊 Progress Tracking**: Console output shows generation progress for longer documents
        - **🎯 Subject-Aware Content**: All generated content is contextually relevant to your chosen subject
        - **📝 Professional Formatting**: Enhanced document structure with proper headings and formatting
        - **🔧 Smart Excel Headers**: Context-aware column names based on your subject area
        
        ## 💡 Subject Examples
        - **Technical**: "machine learning algorithms", "cybersecurity frameworks", "cloud computing"
        - **Business**: "digital transformation", "supply chain management", "customer analytics"  
        - **Industry**: "healthcare innovation", "renewable energy", "financial technology"
        - **Data Protection**: "GDPR compliance", "privacy by design", "data governance"
        
        ## 📄 File Format Features
        - **📝 Word (.docx)**: Formatted documents with headings, paragraphs, lists, and professional styling
        - **📄 Text (.txt)**: Plain text documents with clean formatting for simple content needs
        - **📊 Excel (.xlsx)**: Structured data in spreadsheet format with meaningful, context-aware column headers
        - **📈 CSV (.csv)**: Comma-separated values optimized for data analysis with clean, relevant data
        {'''- **📋 PDF (.pdf)**: Professional PDF documents with advanced typography and formatting''' if REPORTLAB_AVAILABLE else ''}
        """)
    
    return app
