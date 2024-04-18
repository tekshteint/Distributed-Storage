FROM python:3

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Install required packages
RUN apt-get update && \
    apt-get install -y nmap && \
    rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy the Python requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask application files into the container
COPY server.py /app/server.py

# Expose the Flask port
EXPOSE 8080

# Command to start the Flask server
CMD ["python3", "server.py"]
