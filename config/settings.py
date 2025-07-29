"""
Configuration settings for the Synthetic Data Generator
"""

# Try to import reportlab, with fallback
try:
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Dynamic dropdown configurations
file_format_options = {
    "Word Document (.docx)": {
        "formats": ["Word Document (.docx)"],
        "size_options": ["1", "2", "3", "4", "5", "10", "20", "30", "40", "50"],
        "size_label": "Number of Pages",
        "content_options": ["whitepaper", "article", "report", "proposal", "design"], 
        "content_label": "Document Type"
    },
    "Text File (.txt)": {
        "formats": ["Text File (.txt)"],
        "size_options": ["1", "2", "3", "4", "5", "10", "20", "30", "40", "50"],
        "size_label": "Number of Pages",
        "content_options": ["whitepaper", "article", "report", "proposal", "design"], 
        "content_label": "Document Type"
    },
    "Excel Spreadsheet (.xlsx)": {
        "formats": ["Excel Spreadsheet (.xlsx)"],
        "size_options": ["10", "20", "30", "40", "50", "100", "250", "500", "1000", "2000"],
        "size_label": "Number of Rows",
        "content_options": ["5", "10", "15", "20", "25", "30", "50", "100"],
        "content_label": "Number of Columns"
    }, 
    "CSV File (.csv)": {
        "formats": ["CSV File (.csv)"],
        "size_options": ["10", "20", "30", "40", "50", "100", "250", "500", "1000", "2000"],
        "size_label": "Number of Rows",
        "content_options": ["5", "10", "15", "20", "25", "30", "50", "100"],
        "content_label": "Number of Columns"
    }
}

# Add PDF option only if ReportLab is available
if REPORTLAB_AVAILABLE:
    file_format_options["PDF Document (.pdf)"] = {
        "formats": ["PDF Document (.pdf)"],
        "size_options": ["1", "2", "3", "4", "5", "10", "20", "30", "40", "50"],
        "size_label": "Number of Pages",
        "content_options": ["whitepaper", "article", "report", "proposal", "design"], 
        "content_label": "Document Type"
    }
