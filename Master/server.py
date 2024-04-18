from flask import Flask, request, jsonify, send_file
import os
from pathlib import Path
import uuid
import re
import subprocess
import requests
import socket

# Get all local IPs
with open("/ips.txt", "w") as outfile:
    ps = subprocess.Popen(['nmap', '-sn', '172.26.0.0/24'], stdout=subprocess.PIPE)
    output = subprocess.check_output(['grep', '-Eo', '([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)'], stdin=ps.stdout, stderr=subprocess.PIPE) #using grep to filter out the IPs
    ps.wait()

    outfile.write(output.decode("utf-8"))

#Generate a list of local IPs
localIPListPath = "/ips.txt"
with open (localIPListPath, "r") as file:
    localIPs = [line.strip() for line in file]

subprocess.run(["mkdir", "/app/uploads"])
    
sender_ip = socket.gethostbyname(socket.gethostname())
localIPs.remove(sender_ip) #Removing the master's own IP so we don't send the message to ourselves
localIPs.pop(0) #Removing the first IP because it's the gateway
print("LOCAL IPS: ", localIPs)

app =   Flask(__name__) 
UPLOAD_FOLDER = Path(__file__).parent.joinpath('uploads')
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def generateID():
    return str(uuid.uuid4())


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    fileID = generateID()
    file.save(app.config['UPLOAD_FOLDER'] / (fileID + "_" + file.filename + ".whole"))
    FILEPATH = app.config['UPLOAD_FOLDER'] / (fileID + "_" + file.filename + ".whole")
    
    numNodes = len(localIPs)
    fileSize = os.path.getsize(FILEPATH)
    portionSize = fileSize // numNodes
    
    fileSplits = []
    with open(FILEPATH, 'rb') as f:
        for i in range(numNodes):
            start_pos = i * portionSize
            end_pos = (i + 1) * portionSize if i < numNodes - 1 else None
            f.seek(start_pos)
            data = f.read(end_pos - start_pos) if end_pos else f.read()
            fileSplits.append(data)
            
    for i in range(numNodes):
        with open(app.config['UPLOAD_FOLDER'] / (fileID + "_" + file.filename + f".{i}split"), 'wb') as f:
            f.write(fileSplits[i])
            files = {'upload_file': open(f.name, 'rb')}
            r = requests.post(f'http://{localIPs[i]}:8080/upload', files=files)
            if r == requests.codes.ok:
                os.remove(f)
            
    os.remove(FILEPATH)
    
    return jsonify({
        'file_id': fileID
    })



@app.route('/download/<fileID>', methods=['GET'])
def download(fileID):
    for i in localIPs:
        r = requests.get(f'http://{i}:5000/download/{fileID}')
    
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    matchingFiles = [filename for filename in files if fileID in filename]
    
    if len(matchingFiles) == 0:
        return jsonify({'error': 'File not found'})
    
    wholeFile = str(app.config['UPLOAD_FOLDER'] / matchingFiles[0].replace(fileID + "_", ''))
    wholeFileCleaned = re.sub(r'\.[0-9]split+', '', wholeFile)
    
    with open(wholeFileCleaned, 'wb') as f:
        for i in range(len(matchingFiles)):
            with open(app.config['UPLOAD_FOLDER'] / matchingFiles[i], 'rb') as f_split:
                f.write(f_split.read())
                
    return  send_file(wholeFileCleaned, as_attachment=True)
        
    
    

if __name__=='__main__': 
    app.run(debug=True, port=8080, host="0.0.0.0")