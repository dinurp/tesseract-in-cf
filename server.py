import os
import json

from flask import Flask, request, make_response, send_file, Response
from flask import json
from time  import time

import pytesseract

app = Flask(__name__)

#health check
@app.route('/')
def hello():
    return "Hello World"

@app.route('/test')
def test():
    return send_file("test.html")   

@app.route('/ocr', methods=['GET'])
def ocr_test():
    file = request.args.get('image','sample/fox.png')
    lang = request.args.get('lang', 'eng')
    config = request.args.get('config', '--psm 11')
    text = pytesseract.image_to_string(file,lang=lang,config=config)
    response = make_response(text)
    response.headers['Content-Type'] = 'text/plain'
    return response

def getSavedFilepath(folder,filename):
    folder_path = os.path.join("temp",folder)
    os.makedirs(folder_path,exist_ok=True)
    saved_file = os.path.join(folder_path,filename) 
    return saved_file    

@app.route('/ocr', methods=['POST'])
@app.route('/ocr/<folder>', methods=['POST'])
def ocr_files(folder=None):
    folder = folder if  folder else str(time())
    lang = request.args.get('lang', 'eng')
    config = request.args.get('config', '--psm 11')
    uploaded_files = request.files.getlist('image')
    saved_files = []
    for file in uploaded_files:  
        print("Posted file: {}".format(file))
        if file.filename.split('.')[-1] in ['jpeg','png','jpg','pdf','gif','jfif']:
            saved_file = getSavedFilepath(folder,file.filename) 
            file.save( saved_file )
            text = pytesseract.image_to_string(saved_file,lang=lang,config=config)
            saved_files.append({"file":file.filename,"saved_as":saved_file, "text":text}) 
    response = make_response(json.dumps(saved_files))
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('VCAP_APP_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
