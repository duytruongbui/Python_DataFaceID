import cv2
import numpy as np
import pickle
from keras_vggface import utils

def load_stuff(filename):
    saved_stuff = open(filename, "rb")
    stuff = pickle.load(saved_stuff)
    saved_stuff.close()
    return stuff


def pickle_stuff(filename, stuff):
    save_stuff = open(filename, "wb+")
    pickle.dump(stuff, save_stuff)
    save_stuff.close()



def draw_label(image, bbox, label):
    color = [(153, 255, 187), (0, 204, 122)]
    (_w, _h), _ = cv2.getTextSize(label,
                                  cv2.FONT_HERSHEY_DUPLEX,
                                  fontScale=1, thickness=2)

    x, y = bbox[0], bbox[1]
    tl = (bbox[0], bbox[1])
    br = (bbox[2], bbox[3])
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tr = (bbox[0] + w, bbox[1])
    bl = (bbox[2] - w, bbox[1] + h)
    cv2.line(image, tl, (tl[0]+w//3, tl[1]), color[0], 4)
    cv2.line(image, tl, (tl[0], tl[1]+h//3), color[0], 4)

    cv2.line(image, br, (br[0]-w//3, br[1]), color[0], 4)
    cv2.line(image, br, (br[0], br[1]-h//3), color[0], 4)

    cv2.line(image, tr, (tr[0]-w//3, tr[1]), color[0], 4)
    cv2.line(image, tr, (tr[0], tr[1]+h//3), color[0], 4)

    cv2.line(image, bl, (bl[0]+w//3, bl[1]), color[0], 4)
    cv2.line(image, bl, (bl[0], bl[1]-h//3), color[0], 4)

    cv2.rectangle(image, (x, y - _h - 7), (x + _w, y), color[1], cv2.FILLED)
    cv2.putText(image, label, (x, y - _h//4), cv2.FONT_HERSHEY_DUPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)

    return image
