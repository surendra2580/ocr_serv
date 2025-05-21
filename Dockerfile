FROM python:3.9-slim

# Install system dependencies including Tesseract
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/* \
    && tesseract --version

# Set environment variables
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
ENV PATH="/usr/bin:${PATH}"

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
ENV PORT=5000
EXPOSE $PORT

# Command to run the application
CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT 