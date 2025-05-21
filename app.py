from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "OCR Service is running!"

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    extracted_text = pytesseract.image_to_string(image)

    return jsonify({'extracted_text': extracted_text})

if __name__ == '__main__':
    app.run(debug=True) 