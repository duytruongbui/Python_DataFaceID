from itertools import count
import os
import sys
import time

from flask.json import jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import shutil
import base64
import numpy as np
from dotenv import load_dotenv
import cv2
load_dotenv()

def save_face_image(person_type, person_id, images):
    ppId= str(person_id)
    # folder_face_path = os.path.join("./data/faces",ppId)
    folder_face_path = "./database/data/{}".format(ppId)
    print(folder_face_path)
    # folder_face_path = org+folder_face_path
    if os.path.exists(folder_face_path):
        folder_face_path = folder_face_path + "_"+ str(person_type)
    else:
        folder_face_path += "_" + str(person_type)
        os.mkdir(folder_face_path)
    for i, image in enumerate(images):
        img = read_image(image)
        file_path = os.path.join(folder_face_path, "image_{}.jpg".format(i + 1))
        cv2.imwrite(file_path, img)
    time.sleep(3)

def delete_image_database(person_type, peson_id):
    ppIdde = str(peson_id)
    folder_face_path_del = "./database/data/{}".format(ppIdde)
    folder_face_path_del += "_" + str(person_type)
    print(folder_face_path_del)
    if os.path.exists(folder_face_path_del):
        # os.rmdir(folder_face_path_del)
        shutil.rmtree(folder_face_path_del)
    time.sleep(3)

def read_image(file):
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    return image

def decode_image(str):
    image_decode = base64.b64decode(str)
    im_arr = np.frombuffer(image_decode, dtype=np.uint8)
    image_decode2 = cv2.imdecode(im_arr,cv2.IMREAD_COLOR)
    return image_decode2

def prepare_image(image):
    image_content = cv2.imencode(".jpg", image)[1].tostring()
    encoded_image = base64.encodebytes(image_content)
    image_send = "data:image/jpg;base64, " + str(encoded_image, "utf-8")
    return image_send



# extract singal send
def extract_signal_send(request):
    # count_singal = 0
    try:
        raw = request.get_data()
        print(raw)
        # for i in len(raw):
        elements = str(raw.decode('ascii')).split('\r\n')
        info = dict()
        i = 0
        print(elements)
        for element in elements:
            if (element==''):
                break
            print(i)
            key = str(element).split("=")[0]
            value = str(element).split("=")[1]
            info[str(key)]=str(value)
            i= i+1
        return jsonify(info)
    except Exception as e:
        return jsonify({
            "errorCode" : 1,
            "message" : "Fail",
        })

def extract_detail_delete(request):
    count = 0
    try:
        person_type = request.form["personType"]
        count += 1
        person_id = request.form["personId"]
        return (
            person_type,
            person_id,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def extract_detail_register(request):
    count = 0
    try: 
        limit_detail = request.form["limit"]
        count += 1
        offset = request.form["offset"]
        return (
            limit_detail,
            offset,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def extract_detail(request):
    count = 0
    try:
        person_type = request.form["personType"]

        count += 1
        person_id = request.form["personId"]
        count += 1
        image_face_1 = request.files["faceImage1"]
        count += 1

        image_face_2 = request.files["faceImage2"]
        image_face_3 = request.files["faceImage3"]
        image_face_4 = request.files["faceImage4"]
        image_face_5 = request.files["faceImage5"]
        return (
            person_type,
            person_id,
            image_face_1,
            image_face_2,
            image_face_3,
            image_face_4,
            image_face_5,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

