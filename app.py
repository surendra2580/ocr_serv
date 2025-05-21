from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    try:
        # Test if Tesseract is available
        pytesseract.get_tesseract_version()
        return "OCR Service is running!"
    except Exception as e:
        app.logger.error(f"Tesseract error: {str(e)}")
        return "OCR Service is not properly configured. Please check the logs.", 500

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        image = Image.open(image_file.stream)

        extracted_text = pytesseract.image_to_string(image)
        return jsonify({'extracted_text': extracted_text})
    except Exception as e:
        app.logger.error(f"OCR error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
