import os
import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from os.path import join, abspath

app = Flask('catdogvision', template_folder='data/web', static_folder='data/web')

model_path = 'data/models/cat_dog_model.h5'
model = load_model(model_path)

weight_history = []

def load_and_preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return None

    img = load_img(image_path, target_size=(500, 500))
    img = img_to_array(img)
    img = preprocess_input(img)
    return img

def create_model():
    pass

def adjust_model_weights(model, test_image):
    current_weights = model.get_weights()

    weight_history.append(current_weights)
    
def train_model_with_feedback(model, test_image, user_feedback, weight_history, model_path):
    start_time = time.time()

    if user_feedback == 'correct':
        weight_history.append(model.get_weights())
    elif user_feedback == 'incorrect':
        current_weights = model.get_weights()
        predictions_before_update = model.predict(np.array([test_image]))[0][1]

        if predictions_before_update < 0.5:
            optimal_weights = [np.random.standard_normal(w.shape) for w in current_weights]
        else:
            optimal_weights = [np.random.standard_normal(w.shape) for w in current_weights]

        model.set_weights(optimal_weights)
        weight_history.append(optimal_weights)
    else:
        print("Invalid feedback value. Use 'correct' or 'incorrect'.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Training time: {elapsed_time} seconds")

    model.save(model_path)
    print(f"Model saved with updated weights: {model_path}")

def print_weight_history():
    for i, weights in enumerate(weight_history):
        print(f"Iteration {i + 1}: {weights}")

def provide_feedback(model, image, user_feedback):
    current_weights = model.get_weights()
    updated_weights = current_weights  

    updated_model = create_model()
    updated_model.set_weights(updated_weights)

    return updated_model

@app.route('/')
def index():
    uploaded_images_path = 'uploads'
    for filename in os.listdir(uploaded_images_path):
        file_path = os.path.join(uploaded_images_path, filename)
        if filename != 'info.md':  # BLOCK DELETE INFO.MD FILE REMOVE THIS LINE IF YOU WANT (82 Line)
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
        print("Raw Model Output:", predictions)
        probability = predictions[0][1] * 100
        result = "Dog" if probability > 50 else "Cat"

        response_content = jsonify({"prediction": result, "probability": round(probability, 2)}).data.decode('utf-8')
        print(response_content)

        return response_content

@app.route('/feedback', methods=['POST'])
def feedback():
    user_feedback = request.form.get('feedback')
    image_filename = request.form.get('image_path')

    image_path = abspath(join('uploads', image_filename))

    print(f"Feedback received: {user_feedback}")
    print(f"Image path: {image_path}")

    test_image = load_and_preprocess_image(image_path)

    if test_image is None:
        return jsonify({"error": f"File not found: {image_path}"})

    if user_feedback == 'incorrect':
        adjust_model_weights(model, test_image)

    train_model_with_feedback(model, test_image, user_feedback, weight_history, model_path)

    model.save(model_path)
    print(f"Model saved with updated weights: {model_path}")

    print_weight_history()

    return jsonify({"feedback_received": True, "updated_model_path": model_path})

@app.route('/system.js')
def get_system_js():
    return send_file('data/web/system.js')

@app.route('/style.css')
def get_style_css():
    return send_file('data/web/style.css')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)