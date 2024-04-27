FROM python:3

#Set environment variables
ENV FLASK_APP=storageNode.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

#Install required packages
RUN apt-get update && \
    apt-get install -y iputils-ping net-tools telnet  && \
    rm -rf /var/lib/apt/lists/*

#Create and set working directory
WORKDIR /app

#Copy the needed files into the container
COPY requirements.txt /app/requirements.txt
COPY storage.py /app/storage.py

#Install python requirements
RUN pip install -r requirements.txt

#Expose flask port
EXPOSE 8080

#Start the flask server
CMD ["python3", "storage.py"]
