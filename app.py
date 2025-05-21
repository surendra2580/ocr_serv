from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Test if Tesseract is available
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return "OCR Service is running!"
    except Exception as e:
        logger.error(f"Tesseract error: {str(e)}")
        return "OCR Service is not properly configured. Please check the logs.", 500

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            logger.warning("No image uploaded")
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        if not image_file.filename:
            logger.warning("Empty filename")
            return jsonify({'error': 'No image selected'}), 400

        try:
            image = Image.open(image_file.stream)
            logger.info(f"Processing image: {image_file.filename}")
        except Exception as e:
            logger.error(f"Error opening image: {str(e)}")
            return jsonify({'error': 'Invalid image file'}), 400

        try:
            extracted_text = pytesseract.image_to_string(image)
            logger.info("Text extraction successful")
            return jsonify({'extracted_text': extracted_text})
        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}")
            return jsonify({'error': 'Error processing image'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 