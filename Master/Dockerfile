FROM python:3

#Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

#Install required packages
RUN apt-get update && \
    apt-get install -y nmap net-tools iputils-ping telnet && \
    rm -rf /var/lib/apt/lists/*

#Create and set working directory
WORKDIR /app

#Install python requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#Copy the needed files into the container
COPY server.py /app/server.py

#Expose flask port
EXPOSE 8080

#Start the flask server
CMD ["python3", "server.py"]
