import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model

model_path = 'data/models/cat_dog_model.h5'

model = load_model(model_path)

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(64, 64))
    img = img_to_array(img)
    img = preprocess_input(img)
    return img

test_data_dir = 'data/test'

for filename in os.listdir(test_data_dir):
    if filename.endswith(".jpg"):
        image_path = os.path.join(test_data_dir, filename)
        test_image = load_and_preprocess_image(image_path)

        predictions = model.predict(np.array([test_image]))

        if predictions[0][0] > predictions[0][1]:
            result = "Cat"
        else:
            result = "Dog"

        print(f"File: {filename} - Result: {result}")