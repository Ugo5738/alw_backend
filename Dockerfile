# Pull the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary system dependencies
RUN apt-get update -y && \
    apt-get install -y openjdk-17-jdk poppler-utils tesseract-ocr \
    wget gnupg2 netcat-openbsd && \ 
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Install Python dependencies
# RUN pip install -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Give execute permissions to the entrypoint script
RUN chmod +x /code/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/code/entrypoint.sh"]

# Run the application
# CMD daphne alignworkengine.asgi:application --port $PORT --bind 0.0.0.0
CMD ["daphne", "alignworkengine.asgi:application", "--port", "$PORT", "--bind", "0.0.0.0"]