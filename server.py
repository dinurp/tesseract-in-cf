import os
import json

from flask import Flask, request, make_response, send_file, Response
from flask import json

import pytesseract

app = Flask(__name__)

#health check
@app.route('/')
def hello():
    return "Hello World"

@app.route('/ocr')
def tesseract_test():
    file = request.args.get('image','sample/fox.png')
    lang = request.args.get('lang', 'eng')
    config = request.args.get('config', '--psm 11')
    text = pytesseract.image_to_string(file,lang=lang,config=config)
    response = make_response(text)
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('VCAP_APP_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
