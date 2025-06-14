import os
import pytest
from src import main

def test_validate_pdf_nonexistent_file():
    assert not main.validate_pdf("nonexistent.pdf")

def test_validate_pdf_non_pdf_file(tmp_path):
    # Create a dummy text file
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("Not a PDF")
    assert not main.validate_pdf(str(file_path))

def test_extract_merchant_name():
    text = "Walmart Supercenter\n123 Main St\nTotal: $12.34"
    assert main.extract_merchant_name(text) == "Walmart Supercenter"

def test_extract_date():
    text = "Date: 2024-06-15\nTotal: $12.34"
    assert main.extract_date(text) == "2024-06-15"

def test_extract_total_amount():
    text = "Subtotal: $10.00\nTax: $2.34\nTotal: $12.34"
    assert main.extract_total_amount(text) == "12.34"

# Add more tests as needed for your functions