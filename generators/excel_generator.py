"""
Excel and CSV Generator Module
Handles Excel and CSV data generation with smart headers
"""

import pandas as pd
import io
import random
import tempfile

class ExcelGenerator:
    def __init__(self, data_generator):
        self.data_generator = data_generator

    def generate_excel_data(self, rows, columns, subject="business data"):
        """Generate synthetic Excel data with subject context"""
        
        subject_headers = {
            "artificial intelligence": ["AI_Model", "Accuracy_Score", "Training_Data", "Algorithm_Type", "Performance_Metric"],
            "data protection": ["Data_Category", "Protection_Level", "Compliance_Status", "Risk_Score", "Last_Audit"],
            "renewable energy": ["Energy_Source", "Capacity_MW", "Efficiency_Rate", "Location", "Installation_Date"],
            "healthcare": ["Patient_ID", "Treatment_Type", "Outcome_Score", "Duration_Days", "Cost_USD"],
            "finance": ["Transaction_ID", "Amount", "Currency", "Status", "Processing_Date"],
            "marketing": ["Campaign_Name", "Reach", "Engagement_Rate", "ROI_Percent", "Channel"]
        }

        # Try to get subject-specific headers, fallback to generic
        base_headers = None
        for key in subject_headers:
            if key.lower() in subject.lower():
                base_headers = subject_headers[key]
                break
        
        if not base_headers:
            base_headers = ["ID", "Name", "Value", "Status", "Date"]
        
        # Extend or trim headers to match required columns
        if len(base_headers) >= columns:
            headers = base_headers[:columns]
        else:
            headers = base_headers + [f"Field_{i+1}" for i in range(len(base_headers), columns)]
        
        # Create subject-aware prompt for data generation
        prompt = f"""Generate realistic synthetic data for {subject}. Create {rows} rows of data with these columns: {', '.join(headers)}

IMPORTANT: Return ONLY the data rows in CSV format. Do NOT include:
- Column headers
- The word "csv" 
- Any explanatory text
- Quotation marks around the entire response

Format each row as: value1,value2,value3,etc

Generate {rows} rows of realistic data related to {subject}. Make the data contextually appropriate and varied."""

        # Generate content with Ollama
        csv_content = self.data_generator.generate_with_ollama(prompt)
        
        # Parse and create DataFrame
        try:
            # Clean the response more thoroughly
            lines = csv_content.strip().split('\n')
            data_rows = []
            
            print(f"Raw CSV response has {len(lines)} lines")
            
            for line_num, line in enumerate(lines):
                cleaned_line = line.strip()
                
                # Skip problematic lines
                if (not cleaned_line or 
                    cleaned_line.lower().startswith('column_') or
                    cleaned_line.lower().startswith('csv') or
                    cleaned_line.startswith('```') or
                    cleaned_line.lower() in ['', 'data', 'rows', 'format:'] or
                    len(cleaned_line.split(',')) < 2):  # Skip lines with too few columns
                    print(f"Skipping line {line_num}: {cleaned_line}")
                    continue
                
                # Split by comma and clean up each cell
                row = []
                cells = cleaned_line.split(',')
                
                for cell in cells:
                    clean_cell = cell.strip().strip('"').strip("'")
                    row.append(clean_cell)
                
                # Ensure we have the right number of columns
                if len(row) < columns:
                    # Pad with contextual data if needed
                    for i in range(len(row), columns):
                        if i == 0:
                            row.append(f"{subject.replace(' ', '_')}_Item_{len(data_rows)+1}")
                        elif i == 1:
                            row.append(str(random.randint(1, 1000)))
                        elif i == 2:
                            row.append(random.choice(['Active', 'Inactive', 'Pending', 'Complete']))
                        elif i == 3:
                            row.append(f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
                        else:
                            row.append(f"Value_{random.randint(1, 100)}")
                elif len(row) > columns:
                    # Trim if too many columns
                    row = row[:columns]
                
                data_rows.append(row)
                print(f"Added row {len(data_rows)}: {row}")
                
                # Stop if we have enough rows
                if len(data_rows) >= rows:
                    break
            
            print(f"Parsed {len(data_rows)} valid data rows from Ollama response")
            
            # Fill remaining rows if needed with high-quality contextual data
            while len(data_rows) < rows:
                row = []
                for j in range(columns):
                    if j == 0:
                        # First column: ID or name
                        row.append(f"{subject.replace(' ', '_')}_Item_{len(data_rows)+1}")
                    elif j == 1:
                        # Second column: numeric value
                        row.append(str(random.randint(1, 1000)))
                    elif j == 2:
                        # Third column: status or category
                        row.append(random.choice(['Active', 'Inactive', 'Pending', 'Complete', 'Processing', 'Verified']))
                    elif j == 3:
                        # Fourth column: date
                        row.append(f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
                    elif j == 4:
                        # Fifth column: percentage or score
                        row.append(f"{random.randint(1, 100)}%")
                    else:
                        # Additional columns: varied data
                        row.append(f"{subject.replace(' ', '_')}_Data_{random.randint(1, 100)}")
                
                data_rows.append(row)
                print(f"Generated fallback row {len(data_rows)}: {row}")
            
            # Ensure we have exactly the requested number of rows
            data_rows = data_rows[:rows]
            
            # Create DataFrame with proper headers
            df = pd.DataFrame(data_rows, columns=headers)
            print(f"Created DataFrame with shape: {df.shape}")
            print(f"Headers: {list(df.columns)}")
            print(f"First few rows:\n{df.head()}")
            
            return df
            
        except Exception as e:
            print(f"CSV parsing failed: {e}, generating fallback data")
            # Enhanced fallback: generate high-quality contextual synthetic data
            data = []
            for i in range(rows):
                row = []
                for j in range(columns):
                    if j == 0:
                        row.append(f"{subject.replace(' ', '_')}_Item_{i+1}")
                    elif j == 1:
                        row.append(str(random.randint(1, 1000)))
                    elif j == 2:
                        row.append(random.choice(['Active', 'Inactive', 'Pending', 'Complete', 'Processing', 'Verified']))
                    elif j == 3:
                        row.append(f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}")
                    elif j == 4:
                        row.append(f"{random.randint(1, 100)}%")
                    else:
                        row.append(f"{subject.replace(' ', '_')}_Data_{random.randint(1, 100)}")
                data.append(row)
            
            df = pd.DataFrame(data, columns=headers)
            print(f"Created fallback DataFrame with shape: {df.shape}")
            return df

    def create_excel_file(self, df):
        """Create Excel file from DataFrame"""
        excel_bytes = io.BytesIO()
        df.to_excel(excel_bytes, index=False, engine='openpyxl')
        excel_bytes.seek(0)
        return excel_bytes.getvalue()

    def generate_data_file(self, rows, columns, subject, file_format):
        """Main data file generation orchestrator"""
        df = self.generate_excel_data(rows, columns, subject)
        
        if file_format == "Excel Spreadsheet (.xlsx)":
            file_bytes = self.create_excel_file(df)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', prefix='synthetic_') as tmp_file:
                tmp_file.write(file_bytes)
                temp_path = tmp_file.name
        else:  # CSV File (.csv)
            csv_content = df.to_csv(index=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', prefix='synthetic_', mode='w', encoding='utf-8') as tmp_file:
                tmp_file.write(csv_content)
                temp_path = tmp_file.name
        
        return temp_path, f"✅ Generated {rows} rows × {columns} columns about '{subject}' successfully!"