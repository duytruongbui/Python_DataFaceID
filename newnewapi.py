from itertools import count
import os
import re
import time
import base64
import logging
import unicodedata
from tensorflow.python import util

from datetime import date

import sys
import paho.mqtt.client as mqtt

import utilss
from utilss import decode_image, read_image
from flask import Flask, json, request, jsonify
from flask_cors import cross_origin
# from run import precompute_features,recognise_on_image
from datetime import datetime
from main import recognise_on_one_img
from glob import glob
from PIL import Image
import paho.mqtt.client as mqtt
import time, sys

keep_alive = 60


def on_disconnect(client, userdata, flags, rc=0):
    m = "DisConnected flags" + "result code " + str(rc) + "client_id  "
    print(m)
    client.connected_flag = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.connected_flag = True
    else:
        print("Bad connection Returned code=", rc)
        client.bad_connection_flag = True


def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_message(client, userdata, message):
    print("message received  ", str(message.payload.decode("utf-8")))


QOS1 = 1
QOS2 = 0

CLEAN_SESSION = False
port = 1883

#Date Time
today = date.today()

# dd/mm/YY
#now = datetime.now()
nownow = datetime.now()
dt_string = nownow.strftime("%Y/%m/%d %H:%M:%S")



broker = "10.10.20.30"
# broker="124.158.10.175"

client = mqtt.Client("mqttx_2b101d94")
mqtt.Client.connected_flag = False
mqtt.Client.bad_connection_flag = False  #
mqtt.Client.retry_count = 0  #
client.on_connect = on_connect
client.on_disconnect = on_disconnect
run_main = False

app = Flask(__name__)


def extract_face():
    message = {"name": "person_id", "sex": "person_type"}
    return message


@app.route("/api/face-register", methods=["GET", "POST", "DELETE"])
@cross_origin()
def upload():
    path_folder = "./database/data/"
    if request.method == "GET":
        # dataReturn = dict()
        # try:
        request_data_details = utilss.extract_detail_register(request)
        print(len(request_data_details))
        if len(request_data_details) <= 2:
            _, count = request_data_details
            if count == 0:
                lost_field = "limit: int"
                lost_field = "offset: int"
            personArray = []
            for dir in os.listdir(path_folder):
                print(dir)
                personID = dir.split("/")[-1].split("_")[0]
                personType = dir.split("/")[-1].split("_")[1]
                personDict = {
                    "personType": personType,
                    "personId": personID

                }
                personArray.append(personDict)
            dataReturn = {
                "limit": request_data_details[0],
                "offset": request_data_details[1],
                "currentPage": 0,
                "totalPage": 0,
                "face": personArray,
            }
            return jsonify(
                {
                    "errorCode": 0,
                    "data": dataReturn,
                }
            )
        else:
            return jsonify({
                "errorCode": 1,
                "message": "Fail"
            })

    # except:
    #     return jsonify(
    #         {
    #             "errorCode" : 1,
    #             "message" : "Fail"
    #         }
    #     )

    elif request.method == "POST":
        if " " in request.form["personId"]:
            return jsonify({
                "errorCode": 1,
                "message": "Invalid"
            })
        try:
            datatype = ["jpg", "png"]
            check = 1
            request_data = utilss.extract_detail(request)
            for data in request_data[2:]:
                if (data.filename.split(".")[-1] not in datatype):
                    check = 0
            if (check == 0):
                return jsonify({
                    "errorCode": "1",
                    "message": "Type file invalid"

                })

            if len(request_data) < 7:
                _, count = request_data
                if count == 0:
                    lost_field = "person_type: str"
                elif count == 1:
                    lost_field = "person_id: str"
                else:
                    lost_field = "face image: base64, must have five images"
                return jsonify(
                    {
                        "errorCode": 1,
                        "message": lost_field,
                    }
                )

            images = request_data[2:]
            person_type, person_id = request_data[:2]
            utilss.save_face_image(person_type, person_id, images)
            # precompute_features()
            return jsonify({
                "errorCode": 0,
            })
        except Exception as e:
            return jsonify(
                {
                    "errorCode": 1,
                    "message": "Fail",
                }
            )
    else:
        try:
            request_data = utilss.extract_detail_delete(request)
            if len(request_data) < 2:
                _, count = request_data
                if count == 0:
                    lost_field = "person_type: str"
                    lost_field = "person_id: str"
                return jsonify(
                    {
                        "errorCode": 1,
                        "message": lost_field,
                    }
                )

            personidel = request_data[0]
            persontypedel = request_data[1]
            # person_type, person_id = request_data[:2]
            utilss.delete_image_database(personidel, persontypedel)
            # utilss.save_face_image(person_type, person_id, images)
            # precompute_features()
            return jsonify({
                "errorCode": 0
            })
        except Exception as e:
            return jsonify(
                {
                    "errorCode": 1,
                    "message": "Fail",
                }
            )


@app.route("/api/face-recognition", methods=["GET", "POST"])
def recognize():
    if (request.method == "GET"):
        return jsonify("ping success")
    else:
        raw = request.get_data()
        raw_request_send = raw.decode("utf-8")
        elements = str(raw.decode('ascii')).split('\r\n')

        res_back = ""
        info = dict()
        i = 0
        # print(elements)
        for element in elements:
            if (element == ''):
                break
            # print(i)
            key = str(element).split("=")[0]
            value = str(element).split("=")[1]
            if (str(key)!= "AIPictureData"):
                res_back+=str(key)+"="+str(value)+"\n"
            info[str(key)] = str(value)
            i = i + 1

        js_info = info
        # js_info_temp = info
        # print(len(js_info))
        # del js_info_temp['AIPictureData']
        
        #new_js_info = js_info.remove("AIPictureData")
        # raw_result = unicodedata.normalize('NFKD', js_info_temp).encode('ascii', 'ignore')

        fieImgraw = js_info["AIPictureData"]
        fileImg1 = js_info["AIPictureData"]
        # print(fileImg1)

        fileImg1 = fileImg1.replace("\\", "")
        fileImg1 = fileImg1 + "="

        # apipicturelen = str(js_info["AIPictureDataLen"])
        # age = str(js_info["Age"])
        # alarmtime = str(js_info["AlarmTime"])

        devicedIdsignal = str(js_info["DeviceID"])
        # FaceHeight = str(js_info["FaceHeight"])
        # FaceTemperature = str(js_info["FaceTemperature"])
        # FaceWidth = str(js_info["FaceWidth"])
        # FaceX = str(js_info["FaceX"])
        # FaceY = str(js_info["FaceY"])
        # Gender = str(js_info["Gender"])
        # Organ = str(js_info["Organ"])
        # TargeId = str(js_info["TargeId"])
        # TemperatureUnit = str(js_info["TemperatureUnit"])
        # nAlarmType = str(js_info["nAlarmType"])

        fileImg1_new = decode_image(fileImg1)
        bboxes, predict_res = recognise_on_one_img(fileImg1_new)

        new_pic_ss = fileImg1_new[bboxes[0]:bboxes[0]+bboxes[2], bboxes[1]:bboxes[1]+bboxes[3]]
        #new_pic_ss = fileImg1_new.crop(bboxes[1], bboxes[3], bboxes[2], bboxes[4])
        ret, bimg = cv2.imencode('.jpg', new_pic_ss)
        b64img = base64.b64encode(bimg)
        res = dict()
        if (len(bboxes) == 0):
                return jsonify ({
                    "operator": "SnapPush",
                    "info":
                    {
                        "requestRaw": raw_request_send,
                        "personId": "null",
                        "personType": "",
                        "time": dt_string,
                        "similarity": "",
                        "pic": fieImgraw,
                    }
                })
                
                
        for i in range(len(bboxes)):
                person_id, score = predict_res[i]
                if person_id != "?":
                    
                    # res[str(i)] = rec_push
                    rec_push = str(
                        {
                            "operator": "RecPush",
                            "info":
                            {
                                "requestRaw": raw_request_send,
                                "personId": person_id,
                                "personType": 0,
                                "time": dt_string,
                                "similarity": score,
                                "faceCoordinates": bboxes[i][:4],
                                "pic": fieImgraw,
                            }
                        }
                    )
                    return jsonify(rec_push)
                else:
                    return jsonify({
                        "operator": "SnapPush",
                        "info":
                        {
                            "requestRaw": raw_request_send,
                            "personId": "",
                            "personType": "",
                            "time": dt_string,
                            "similarity": "",
                            "pic": fieImgraw,
                        }
                    })
                    
                    


@app.route("/recognition", methods=["GET", "POST"])
@cross_origin()
def recognition():
    if request.method == "POST":
        message = {
            "status": "0",
            "message": "cannot POST /recognition, not allow POST method in url",
        }
        return jsonify(message)
    else:
        message = extract_face()
        return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)




