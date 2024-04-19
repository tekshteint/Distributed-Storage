from flask import Flask, request, jsonify, send_file
import os
import http

app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return "200"
    else:
        return "400"


@app.route('/download/<fileID>', methods=['GET'])
def download(fileID):
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    matchingFiles = [filename for filename in files if fileID in filename]
    
    if len(matchingFiles) == 0:
        return jsonify({'error': 'File not found'})
    
    partialFile = str(app.config['UPLOAD_FOLDER'] / matchingFiles[0].replace(fileID + "_", ''))
    
                
    return  send_file(partialFile, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
    
