# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask PyMuPDF pyspellchecker

# Expose the web server port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
