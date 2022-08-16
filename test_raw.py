import base64
from flask import Flask, request, jsonify
import requests

import json

from utilss import decode_image

app = Flask(__name__)


@app.route('/foo', methods=['POST'])
def foo():
    raw = request.get_data()
    # print(raw)
    # for i in len(raw):
    elements = str(raw.decode('ascii')).split('\r\n')
    info = dict()
    i = 0
    print(elements)
    for element in elements:
        if (element == ''):
            break
        key = str(element).split("=")[0]
        value = str(element).split("=")[1]
        info[str(key)] = str(value)
    imgFile = info["AIPictureData"]
    imgString = imgFile.replace("\\","")
    imgString = imgString +"="
    imgdata = base64.b64decode(imgString)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)
    # print(imgString)
    # with open('convert.js', 'w') as convert_file:
    #     convert_file.write(json.dumps(info))
    return imgString


    



app.run("127.0.0.1", port=80)