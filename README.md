# OCR Service

A simple Flask-based OCR (Optical Character Recognition) service that extracts text from images.

## Features

- REST API endpoint for OCR processing
- Supports image upload and text extraction
- Docker containerization for easy deployment
- Ready for deployment on Render

## Prerequisites

- Python 3.9+
- Tesseract OCR
- Docker (for containerized deployment)

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The service will be available at `http://localhost:5000`

## API Usage

### Extract Text from Image

**Endpoint:** `POST /ocr`

**Request:**
- Content-Type: multipart/form-data
- Body: Form data with key 'image' containing the image file

**Response:**
```json
{
    "extracted_text": "Text extracted from the image"
}
```

## Deployment

The service is configured for deployment on Render using Docker. The `render.yaml` file contains the necessary configuration.

## License

MIT 