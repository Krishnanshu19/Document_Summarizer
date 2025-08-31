# Document Summarizer

## Overview
This is a document summarizer application built using Flask and the Hugging Face Transformers library. It allows users to upload PDF or image files, extract text, and generate summaries based on their chosen summary length (short, medium, or long).

## Features
- Upload PDF and image files (JPEG, PNG, JPG).
- Extract text from the uploaded files using OCR (Optical Character Recognition) for images and text extraction for PDFs.
- Summarize the extracted text using Hugging Face's BART model.
- Choose the length of the summary (short, medium, long).

## Technologies Used
- **Flask**: Web framework for building the backend.
- **Hugging Face Transformers**: BART model for text summarization.
- **Tesseract OCR**: For extracting text from images.
- **PyMuPDF (fitz)**: For extracting text from PDFs.
- **HTML/CSS**: For the frontend to upload files and display summaries.
- **JavaScript (Optional)**: For adding interactivity and a spinner during processing.

## Setup and Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/document-summarizer.git
cd document-summarizer
2. Create a virtual environment
It's recommended to use a virtual environment to manage dependencies.

bash
Copy
Edit
python3 -m venv summarizer-env
3. Activate the virtual environment
On Windows:
bash
Copy
Edit
summarizer-env\Scripts\activate
On macOS/Linux:
bash
Copy
Edit
source summarizer-env/bin/activate
4. Install the required dependencies
bash
Copy
Edit
pip install -r requirements.txt
requirements.txt should include the following dependencies:

plaintext
Copy
Edit
flask
transformers
pillow
pytesseract
fitz
flask-cors
Additionally, ensure that Tesseract OCR is installed on your system. You can download it from Tesseract GitHub or here for Windows.

For image processing, you will also need Poppler installed for PDF-to-image conversion (used by pdf2image). You can download it from here.

5. Set up the Tesseract path (Windows)
You need to specify the Tesseract executable path in your script (adjust the path as needed):

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
6. Run the application
To start the Flask server, run:

bash
Copy
Edit
python app.py
This will start the app on http://127.0.0.1:5000/.

7. Frontend
You can now open your browser and visit the application in the local development environment.

How It Works
Upload a File: The user can upload a PDF or image file using the web interface.

Text Extraction:

For PDFs, the app extracts text using the PyMuPDF library (fitz).

For images, Tesseract OCR is used to extract text.

Summarization: Once the text is extracted, the Hugging Face model (facebook/bart-large-cnn) generates a summary based on the chosen length (short, medium, or long).

Display Summary: The generated summary is displayed on the webpage.

API Endpoints
/upload (POST)
Description: Upload a file and receive a text summary.

Parameters:

file: The file to upload (PDF or image).

length: (Optional) The length of the summary (short, medium, or long). Default is medium.

Example Response:
json
Copy
Edit
{
  "message": "File uploaded, text extracted, and summarized",
  "filename": "example.pdf",
  "summary": "This is a short summary of the uploaded document."
}
Frontend
The frontend is a simple HTML form where users can upload files and select summary length. It will display a loading spinner while the backend processes the file.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Flask

Transformers

PyMuPDF

Tesseract OCR

Poppler

markdown
Copy
Edit

---

### Key Sections in the README:
- **Overview**: Provides a summary of the project and what it does.
- **Features**: Lists the main features of the app.
- **Technologies Used**: Describes the technologies and libraries that are used in the app.
- **Setup and Installation**: Explains how to set up the project locally.
- **API Endpoints**: Documents the API routes that are available to interact with the backend.
- **License**: Adds a basic license section for the project (MIT License is used here).
