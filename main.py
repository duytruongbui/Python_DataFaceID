import cv2
import os
import time
import numpy as np
from matplotlib import pyplot as plt
import os
import click
from core.face_identity import FaceIdentify

face_engine = FaceIdentify()



def recognise_on_image(img_path, compute_feature):
    if compute_feature:
        face_engine.precompute_features()

    img = cv2.imread(img_path)
    img_show, predicted_names = face_engine._inference_on_image(img)

    cv2.imwrite('out.png', img_show)

def recognise_on_one_img(img):
    bboxes, predicted_result = face_engine._inference_on_image(img)
    return bboxes,predicted_result



def recognise_on_video(src, is_show, compute_feature):
    cap = cv2.VideoCapture(src)
    w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(w, h, fps)
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w,h))

    if compute_feature:
        face_engine.precompute_features()

    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            img_show, predicted_names = face_engine._inference_on_image(img)
            out.write(img_show)
            if is_show:
                cv2.imshow('out', img_show)


            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
              break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

@click.command()
@click.option('--is_video', '-v', is_flag=True, help='flag on if run on video - image in otherwise')
@click.option('--compute_feature', '-c', is_flag=True, help='Run compute features first if True')
@click.option('--show', '-s', is_flag=True, help="Show the result on screen")
@click.option('--src', help='Path to image or video')
def main(is_video, compute_feature, show, src):
    # print(is_video, compute_feature, output, src)
    if src is None:
        print('Source is None')
        return

    if is_video:
        recognise_on_video(src, show, compute_feature)
    else:
        recognise_on_image(src, compute_feature)

if __name__ == '__main__':
    main()
