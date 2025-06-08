# Receipt OCR Extractor 🧾🔍

A Python-based system that extracts structured data like merchant name, purchase date, and total amount from scanned or image-based receipt PDFs using OCR (Optical Character Recognition).

## 🚀 Features

- 📄 Supports scanned or image-based PDF receipts
- 🧠 Uses Tesseract OCR via `pytesseract` for text extraction
- 🛒 Automatically extracts:
  - Merchant Name
  - Purchase Date
  - Total Amount
- 📋 Outputs structured data via pandas DataFrame

## 🗂 Project Structure

    receipt-ocr-extractor/
    ├── src/
    │ └── main.py # Main script with logic
    ├── receipts/ # PDF input files
    ├── requirements.txt # Dependencies
    ├── README.md
    └── .gitignore

## ⚙️ Setup

1. **Clone the repo**:

   ```bash
   git clone https://github.com/your-username/receipt-ocr-extractor.git
   cd receipt-ocr-extractor

   ```

2. **Create a virtual environment**:
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate on Windows

3. **Install dependencies:**:
   pip install -r requirements.txt

## Additional Requirements

1. **Tesseract OCR**
   Used by pytesseract to extract text from images

✅ Install Tesseract
Windows:

    Download: https://github.com/tesseract-ocr/tesseract

    After install, add the path to tesseract.exe (e.g., C:\Program Files\Tesseract-OCR) to your System Environment Variables > PATH

macOS:
brew install tesseract

Linux (Debian/Ubuntu):
sudo apt update
sudo apt install tesseract-ocr

2.  **Poppler for PDF Rendering**:
    Used by pdf2image to convert PDF pages into images.

        ✅ Install Poppler
        Windows:

            Download: https://github.com/oschwartz10612/poppler-windows/releases/

            Extract and add the bin/ directory to your System PATH

        macOS:
            brew install poppler

        Linux (Debian/Ubuntu):
                sudo apt update
                sudo apt install poppler-utils

## Run the Script

Edit the Config class in src/main.py to set the CURRENT_FILE, then run:

    python src/main.py

## Example Output

    merchant_name   : Old Navy
    purchased_at    : 2024-05-28 15:30:00
    total_amount    : 75.42

Built with 💻 by Balaji and 🤖 Claude AI
