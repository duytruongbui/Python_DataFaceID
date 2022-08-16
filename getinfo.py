from flask import Flask, request, jsonify
import requests

import json
with open('convert.js') as datajs:
    data = json.load(datajs)
    value = data["AIPictureData"]
    value2 = data["AIPictureDataLen"]
    # print(str(value))

    

    value_new = value.replace("\\","")
    f = open("abcd.txt", "a")
    f.write(str(value_new))