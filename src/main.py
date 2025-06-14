
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
import pandas as pd
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from dateutil import parser as date_parser


class Config:
    # Update this path to your receipt files directory
    RECEIPTS_DIR = "./receipts"  # Change filename here for testing
    CURRENT_FILE = "oldnavy_20240528_006.pdf"  # Change this to test different files
    


print("=== Receipt Information Extraction System ===")
print(f"Current file to process: {Config.CURRENT_FILE}")
print(f"Looking in directory: {Config.RECEIPTS_DIR}")


def validate_pdf(file_path):
    """
    Validate if the file is a valid PDF
    Returns: (is_valid, error_message)
    """
    try:
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        if not file_path.lower().endswith('.pdf'):
            return False, "File is not a PDF"
        
        # Try to open and read the PDF
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            if num_pages == 0:
                return False, "PDF has no pages"
            
            print(f"✓ Valid PDF with {num_pages} page(s)")
            return True, f"Valid PDF with {num_pages} pages"
            
    except Exception as e:
        return False, f"PDF validation error: {str(e)}"


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using OCR (pdf2image + tesseract)
    Returns: extracted text string
    """
    try:
        print("Converting PDF to images...")
        # Convert PDF to images
        images = convert_from_path(file_path, dpi=300)
        
        extracted_text = ""
        
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)}")
            
            # Use OCR to extract text from image
            page_text = pytesseract.image_to_string(image, config='--psm 6')
            extracted_text += f"\n--- Page {i+1} ---\n" + page_text
        
        return extracted_text
        
    except Exception as e:
        print(f"OCR extraction error: {str(e)}")
        return ""


def extract_merchant_name(text):
    """Extract merchant name from receipt text"""
    lines = text.split('\n')
    
    # Common patterns for merchant names (usually at the top)
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        line = line.strip()
        if len(line) > 2 and not re.match(r'^[\d\s\-\.\,\$]+$', line):
            # Skip common non-merchant patterns
            skip_patterns = [
                r'receipt', r'invoice', r'bill', r'thank you', 
                r'page \d+', r'^\d+$', r'date', r'time'
            ]
            
            if not any(re.search(pattern, line.lower()) for pattern in skip_patterns):
                if len(line) > 3:  # Reasonable merchant name length
                    return line
    
    return "Unknown Merchant"


def extract_date(text):
    """Extract purchase date from receipt text"""
    # Common date patterns
    date_patterns = [
        r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b(\d{2,4}[\/\-]\d{1,2}[\/\-]\d{1,2})\b',  # YYYY/MM/DD or YYYY-MM-DD
        r'\b([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4})\b',  # Month DD, YYYY
        r'\b(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\b',    # DD Month YYYY
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                # Try to parse the date
                parsed_date = date_parser.parse(match, fuzzy=True)
                return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            except:
                continue
    
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def extract_total_amount(text):
    """Extract total amount from receipt text"""
    # Look for total patterns
    total_patterns = [
        r'total[:\s]*\$?(\d+\.?\d*)',
        r'amount[:\s]*\$?(\d+\.?\d*)',
        r'sum[:\s]*\$?(\d+\.?\d*)',
        r'\$(\d+\.\d{2})\s*$',  # Dollar amount at end of line
        r'(\d+\.\d{2})\s*total',
    ]
    
    lines = text.lower().split('\n')
    amounts = []
    
    for line in lines:
        for pattern in total_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                try:
                    amount = float(match)
                    if 0.01 <= amount <= 10000:  # Reasonable amount range
                        amounts.append(amount)
                except:
                    continue
    
    # Return the largest reasonable amount (likely the total)
    return max(amounts) if amounts else 0.0


def process_receipt(file_path):
    """
    Main function to process a single receipt
    Returns: dictionary with extracted information
    """
    print(f"\n{'='*50}")
    print(f"Processing: {os.path.basename(file_path)}")
    print(f"{'='*50}")
    
    # Step 1: Validate PDF
    is_valid, message = validate_pdf(file_path)
    if not is_valid:
        print(f"❌ Validation failed: {message}")
        return None
    
    # Step 2: Extract text using OCR
    print("\n📄 Extracting text using OCR...")
    extracted_text = extract_text_from_pdf(file_path)
    
    if not extracted_text.strip():
        print("❌ No text could be extracted from PDF")
        return None
    
    print("✓ Text extraction completed")
    
    # Step 3: Parse information
    print("\n🔍 Parsing receipt information...")
    
    receipt_data = {
        'id': str(uuid.uuid4()),
        'purchased_at': extract_date(extracted_text),
        'merchant_name': extract_merchant_name(extracted_text),
        'total_amount': extract_total_amount(extracted_text)
    }
    
    return receipt_data, extracted_text


def test_current_file():
    """Test the currently configured file"""
    file_path = os.path.join(Config.RECEIPTS_DIR, Config.CURRENT_FILE)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("Please check the file path and name in the Config class")
        return
    
    result = process_receipt(file_path)
    
    if result:
        receipt_data, extracted_text = result
        
        # Display results
        print(f"\n{'='*50}")
        print("📊 EXTRACTED INFORMATION")
        print(f"{'='*50}")
        
        for key, value in receipt_data.items():
            print(f"{key:15}: {value}")
        
        print(f"\n{'='*50}")
        print("📝 RAW EXTRACTED TEXT")
        print(f"{'='*50}")
        print(extracted_text)
        
        # Create DataFrame for better display
        df = pd.DataFrame([receipt_data])
        print(f"\n{'='*50}")
        print("📋 STRUCTURED DATA")
        print(f"{'='*50}")
        print(df.to_string(index=False))
        
        return receipt_data
    else:
        print("❌ Failed to process receipt")
        return None

if __name__ == "__main__":
    print("Starting receipt processing test...")
    result = test_current_file()


