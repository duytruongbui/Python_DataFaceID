import cv2
import os
import time
import argparse
import numpy as np
from matplotlib import pyplot as plt
from .utils import draw_label, pickle_stuff, load_stuff
from .face_extractor.extractor import FaceExtractor
from .face_detector.lib.core.api.face_detector import FaceDetector
import os
from scipy.spatial.distance import euclidean
from tqdm import tqdm
import click


class FaceIdentify:
    def __init__(self, face_size=(224, 224)):
        print("Loading Detector model ...")
        self.detector = FaceDetector('core/face_detector/weight')
        print("Loading Detector model: Done")

        print("Loading Extractor model ...")
        self.extractor = FaceExtractor(input_shape=face_size+(3,))
        print("Loading Extractor model: Done")

        print("Loading database ...")
        self.database = load_stuff("database/database.pickle")
        print("Loading database: Done")

    def compute_mean_feature(self, face_images):
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

        batch_size = 32
        face_images_chunks = chunks(face_images, batch_size)
        fvecs = None
        for face_images_chunk in face_images_chunks:
            batch_fvecs = self.extractor.extract(face_images_chunk)
            if fvecs is None:
                fvecs = batch_fvecs
            else:
                fvecs = np.append(fvecs, batch_fvecs, axis=0)
        return np.array(fvecs).sum(axis=0) / len(fvecs)

    def precompute_features(self, image_folder='database/data/frames'):
        database = []
        identities = os.listdir(image_folder)
        # for each identity in database
        out_root = 'database/data/faces'
        if not os.path.exists(out_root):
            os.mkdir(out_root)
        for i in tqdm(range(len(identities))):
            identity = identities[i]
            out_path = os.path.join(out_root, identity)
            if not os.path.exists(out_path):
                os.mkdir(out_path)

            # crop faces
            face_imgs = []
            for img_name in os.listdir(os.path.join(image_folder, identity)):
                img_path = os.path.join(image_folder, identity, img_name)
                image = cv2.imread(img_path)
                bboxes = self.detector.detect_face(image)

                for bbox in bboxes:
                    face_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                    face_imgs.append(face_img)

            for i, img in enumerate(face_imgs):
                cv2.imwrite(os.path.join(out_path, '%02d.png'%(i+1)), img)

            # compute mean features
            mean_features = self.compute_mean_feature(face_imgs)
            database.append({"name": identity, "features": mean_features})

        pickle_stuff("database/database.pickle",  database)


    def identify_face(self, features, threshold=90):
        if len(self.database) > 0:
            distances = []
            for person in self.database:
                person_features = person.get("features")
                distance = euclidean(person_features, features)
                distances.append(distance)

            min_distance_value = min(distances)
            min_distance_index = distances.index(min_distance_value)
            normalize_distance = 100-(abs(min_distance_value-threshold)/threshold)
            print(min_distance_value, self.database[min_distance_index].get("name"))
            if min_distance_value < threshold:
                return self.database[min_distance_index].get("name"),normalize_distance
            else:
                return "?",100
        else:
            return "?",100

    def add_new_identity(self):
        pass

    def _inference_on_image(self, img):
        # cv2.imwrite("test.jpg",img)
        img_show = img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bboxes = self.detector.detect_face(img, threshold=0.7)

        # crop face image
        face_imgs = []
        for bbox in bboxes:
            face_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            face_imgs.append(face_img)

        # recognise for each face
        predicted_result = []
        if len(face_imgs) > 0:
            # generate features for each face
            features_faces = self.extractor.extract(face_imgs)
            predicted_result = [self.identify_face(features_face) for features_face in features_faces]


            # for bbox, predicted_name in zip(bboxes, predicted_names):
            #     img_show = draw_label(img_show, bbox, predicted_name)

        # return img_show, predicted_names
        return bboxes,predicted_result
