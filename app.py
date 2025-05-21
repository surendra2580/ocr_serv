from flask import Flask, request, jsonify, render_template_string
from PIL import Image
import pytesseract
import os
import logging
import sys
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Set Tesseract path based on the operating system
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ZEN59\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Verify Tesseract installation
try:
    version = pytesseract.get_tesseract_version()
    logger.info(f"Tesseract version: {version}")
except Exception as e:
    logger.error(f"Tesseract error: {str(e)}")

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>OCR Service</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .upload-form {
            margin: 20px 0;
            text-align: center;
        }
        .file-input {
            margin: 10px 0;
        }
        .submit-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .submit-btn:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #f9f9f9;
            white-space: pre-wrap;
        }
        .error {
            color: red;
            text-align: center;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OCR Service</h1>
        <div class="upload-form">
            <form action="/ocr" method="post" enctype="multipart/form-data">
                <div class="file-input">
                    <input type="file" name="image" accept="image/*" required>
                </div>
                <button type="submit" class="submit-btn">Extract Text</button>
            </form>
        </div>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        {% if extracted_text %}
        <div class="result">
            <h3>Extracted Text:</h3>
            <p>{{ extracted_text }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    try:
        # Test if Tesseract is available
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return render_template_string(HTML_TEMPLATE)
    except Exception as e:
        logger.error(f"Tesseract error: {str(e)}")
        return render_template_string(HTML_TEMPLATE, error="OCR Service is not properly configured. Please check the logs.")

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            logger.warning("No image uploaded")
            return render_template_string(HTML_TEMPLATE, error="No image uploaded")

        image_file = request.files['image']
        if not image_file.filename:
            logger.warning("Empty filename")
            return render_template_string(HTML_TEMPLATE, error="No image selected")

        try:
            image = Image.open(image_file.stream)
            logger.info(f"Processing image: {image_file.filename}")
        except Exception as e:
            logger.error(f"Error opening image: {str(e)}")
            return render_template_string(HTML_TEMPLATE, error="Invalid image file")

        try:
            extracted_text = pytesseract.image_to_string(image)
            logger.info("Text extraction successful")
            return render_template_string(HTML_TEMPLATE, extracted_text=extracted_text)
        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}")
            return render_template_string(HTML_TEMPLATE, error="Error processing image")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return render_template_string(HTML_TEMPLATE, error="Internal server error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 