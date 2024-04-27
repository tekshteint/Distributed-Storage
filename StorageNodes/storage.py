from flask import Flask, request, jsonify, send_file
import os
import sys 

app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Add the upload folder to the app configuration

@app.route('/upload', methods=['POST'])
def upload():
    """File upload endpoint used by the Master Node

    Returns:
        HTTP response code
    """
    file = request.files['file']

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename)) #If a file is present, return OK
        return "200"
    else:
        return "400" #Return Bad Request if no file is present


@app.route('/download/<fileID>', methods=['GET'])
def download(fileID):
    """Download file endpoint

    Args:
        fileID (str): A given file's UUID which was generated when uploaded

    Returns:
        Uploaded file slice
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    matchingFiles = [filename for filename in files if fileID in filename] #Finds matching files based on their UUID
    
    if len(matchingFiles) == 0:
        return jsonify({'error': 'File not found'})
    
    
                
    return  send_file("/uploads/" + matchingFiles[0], as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
    
