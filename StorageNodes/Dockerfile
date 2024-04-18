FROM python:3

# Set environment variables
ENV FLASK_APP=storageNode.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Create and set working directory
WORKDIR /app

# Copy the Python file into the container
COPY requirements.txt /app/requirements.txt
COPY storage.py /app/storage.py

# Install required packages
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to start the Flask application
CMD ["python3", "storage.py"]
