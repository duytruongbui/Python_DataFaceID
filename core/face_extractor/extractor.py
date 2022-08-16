import cv2
import os
import time
import numpy as np
from keras_vggface.vggface import VGGFace
from keras_vggface import utils

def preprocess_data(x):
    x = [cv2.resize(img, (224, 224)) for img in x]
    x = np.array(x, dtype='float16')
    x = utils.preprocess_input(x, version=1)

    return x


class FaceExtractor:
    def __init__(self,
                 backbone='resnet50',
                 include_top=False,
                 input_shape=(224, 224, 3)):

        self.model = VGGFace(model=backbone,
                        include_top=include_top,
                        input_shape=input_shape,
                        pooling='avg')

    def extract(self, face_imgs):
        inputs = preprocess_data(face_imgs)
        features_faces = self.model.predict(inputs)

        return features_faces

    def identify_face(self, features, database, threshold=100):
        if len(database) > 0:
            distances = []
            for person in database:
                person_features = person.get("features")
                distance = euclidean(person_features, features)
                distances.append(distance)

            min_distance_value = min(distances)
            min_distance_index = distances.index(min_distance_value)
            print(min_distance_value, database[min_distance_index].get("name"))
            if min_distance_value < threshold:
                return database[min_distance_index].get("name")
            else:
                return "?"

        else:
            return "?"
