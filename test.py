import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask('catdogvision', template_folder='data/web')
model_path = 'data/models/cat_dog_model.h5'

model = load_model(model_path)

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(500, 500))
    img = img_to_array(img)
    img = preprocess_input(img)
    return img

@app.route('/')
def index():
    uploaded_images_path = 'uploads'
    for filename in os.listdir(uploaded_images_path):
        file_path = os.path.join(uploaded_images_path, filename)
        os.remove(file_path)

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join('uploads', filename)
        file.save(image_path)
        test_image = load_and_preprocess_image(image_path)
        predictions = model.predict(np.array([test_image]))
        probability = predictions[0][1] * 100
        result = "Dog" if probability > 50 else "Cat"
        return jsonify({"prediction": result, "probability": round(probability, 2)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)