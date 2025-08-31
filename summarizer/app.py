from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from transformers import pipeline
from flask_cors import CORS
import fitz  # PyMuPDF (for PDF text extraction)
import pytesseract
from PIL import Image, ImageOps

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the path to Tesseract executable (for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Krishnanshu Agrawal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Initialize Hugging Face summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpeg', 'png', 'jpg'}

# Create the uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Function to preprocess and extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        
        # Preprocess the image: Convert to grayscale and auto-adjust contrast
        img = ImageOps.exif_transpose(img).convert("L")
        img = ImageOps.autocontrast(img)
        
        text = pytesseract.image_to_string(img)
        print(f"Extracted text from image: {text}")  # Debugging output
        
        if not text.strip():
            raise ValueError("No text extracted from image.")
        
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

# Function to summarize the extracted text
def summarize_text(text, length="medium"):
    if length == "short":
        min_length = 50
        max_length = 150
    elif length == "medium":
        min_length = 150
        max_length = 300
    else:  # long summary
        min_length = 300
        max_length = 600

    summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)
    return summary[0]['summary_text']

# Route for file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Debugging: Print file information
    print(f"Uploaded file: {file.filename}, Type: {file.content_type}")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # Save the uploaded file to the server
            file.save(filepath)
            print(f"File saved at: {filepath}")
            
            # Extract text from the uploaded file
            if filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(filepath)
            else:
                text = extract_text_from_image(filepath)
            
            # If no text was extracted, return an error
            if not text:
                return jsonify({"error": "Text extraction failed"}), 400
            
            # Get summary length from query params (defaults to 'medium')
            summary_length = request.args.get('length', 'medium')  # Short, Medium, or Long
            summary = summarize_text(text, length=summary_length)

            # Return the summary and status message
            return jsonify({
                "message": "File uploaded, text extracted, and summarized",
                "filename": filename,
                "summary": summary
            }), 200
        
        except Exception as e:
            return jsonify({"error": f"Error processing the file: {str(e)}"}), 500
    
    else:
        return jsonify({"error": "Invalid file format"}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
