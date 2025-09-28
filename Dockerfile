# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi


# Expose a volume for data.json persistence in the project root
VOLUME ["/app/data.json"]

# Set environment variable for data path (optional, can be used in your code)
ENV DATA_PATH=/app/data.json

# Default command (adjust as needed)
CMD ["python", "optimized_main.py"]
