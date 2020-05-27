import os

from flask import Flask, request, make_response, send_file, Response
from flask import json
from time  import time

import pytesseract

import logging 
logger = logging.getLogger('tesseract-in-cf')
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
    logger.info("pytesseract.image_to_string({},lang={},config={})".format(file,lang,config))
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
        logger.info("Posted file: {}".format(file))
        if file.filename.split('.')[-1] in ['jpeg','png','jpg','pdf','gif','jfif']:
            saved_file = getSavedFilepath(folder,file.filename) 
            file.save( saved_file )
            logger.info("pytesseract.image_to_string({},lang={},config={})".format(saved_file,lang,config))
            text = pytesseract.image_to_string(saved_file,lang=lang,config=config)
            saved_files.append({"file":file.filename,"saved_as":saved_file, "text":text}) 
    response = make_response(json.dumps(saved_files))
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    import logging.config
    import yaml

    with open('logger-config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('VCAP_APP_HOST', '0.0.0.0')
    app.run(host=host, port=port)
