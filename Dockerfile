# Use Python 3.9 base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Python script
COPY app.py .

# Run the Python script on container startup
CMD ["python", "app.py"]



