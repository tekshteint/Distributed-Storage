FROM python:3

# Set environment variables
ENV FLASK_APP=storageNode.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Install required packages
RUN pip install -r requirements.txt

# Create and set working directory
WORKDIR /app

# Copy the Python file into the container
COPY storage.py /app/storage.py

# Expose the Flask port
EXPOSE 5000

# Command to start the Flask application
CMD ["flask", "run"]
