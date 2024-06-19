import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import bcrypt
import io
import base64
import numpy as np
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from dotenv import load_dotenv

#import tensorflow as tf

load_dotenv("var.env")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

class TextInputForm(FlaskForm):
    text_input = TextAreaField('Text Input', validators=[DataRequired()])


def process_password(password, confirm_password):
    if len(password) < 8:
        message = 'Password should have a minimum of 8 characters'
        return render_template('login.html', signupmessage=message)

    if len(password) > 16:
        message = 'Password should have a maximum of 16 characters'
        return render_template('login.html', signupmessage=message)

    numbers = "1234567890"
    if any(c in numbers for c in password):
        pass
    else:
        message = 'Password should contain numbers'
        return render_template('login.html', signupmessage=message)

    special_characters = "'!@# $%^&*()-+?_=,<>/'"
    if any(c in special_characters for c in password):
        pass
    else:
        message = 'Password should contain any special characters'
        return render_template('login.html', signupmessage=message)

    if password != confirm_password:
        message = 'Passwords do not match, please try again.'
        return render_template('login.html', signupmessage=message)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_password


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if 'username' in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        if 'signup' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            hashed_password = process_password(password, confirm_password)

            users = mongo.db.users
            existing_username = users.find_one({'username': username})
            existing_email = users.find_one({'email': email})

            if existing_username is not None:
                message = 'Username already exists.'
                return render_template('login.html', signupmessage=message)

            if existing_email is not None:
                message = 'Email already exists.'
                return render_template('login.html', signupmessage=message)

            users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            return render_template('signup_success.html')

        elif 'login' in request.form:
            username = request.form['username']
            password = request.form['password']

            users = mongo.db.users
            login_user = users.find_one({'username': username})

            if login_user and bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
                session['username'] = username
                return redirect(url_for('chat'))
            else:
                message = 'Invalid username or password. Please try again.'
                return render_template('login.html', message=message)
        return redirect(url_for('profile'))

    return render_template('login.html', message=message)


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    username = session['username']
    message =  ''
    status = ''

    users = mongo.db.users
    login_user = users.find_one({'username': username})

    email = login_user['email']

    if request.method == 'POST':
        new_username = request.form['username']
        print("new username: ", new_username)
        new_email = request.form['email']
        new_password = request.form['password']
        new_confirm_password = request.form['confirm_password']

        if new_username != '':
            if (new_username == username):
                message = "New username can't be same as old username"
            else:
                existing_username = users.find_one({'username': new_username})
                if existing_username is not None:
                        message = 'Username already exists.'
                else:
                    users.update_one({'username': username}, {'$set': {'username': new_username}})
                    status='Username updated'
                    username = new_username
                    session['username'] = username
        
        if new_email != '':
            if (new_email == email):
                message = "New email can't be same as old email"
            else:
                existing_email = users.find_one({'email': new_email})
                if existing_email is not None:
                        message = 'Email already exists.'
                else:
                    users.update_one({'email': email}, {'$set': {'email': new_email}})
                    status='Email updated'
                    email = new_email
        
        if new_password != '':
            hashed_password = process_password(new_password, new_confirm_password)
            users.update_one({'username': username}, {'$set': {'password': hashed_password}})
            status='Password updated'

    return render_template('profile.html', username=username, email=email, message=message, status=status)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():

    with open("images/photo.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    messages = [['bot', 'text', 'Hello, How may I assist you today?'],
                ['user', 'text', 'I need assistance in identifying a plant disease. It is very hard for me to find it manually.'],
                ['bot', 'text', 'Sure, send me the plant image.'],
                ['user', 'image', encoded_string],
                ['bot', 'text', 'Hello, How may I assist you today?'],
                ['user', 'text', 'I need assistance in identifying a plant disease. It is very hard for me to find it manually.'],
                ['bot', 'text', 'Sure, send me the plant image.'],
                ['user', 'image', encoded_string]]

    form = TextInputForm()
    if form.validate_on_submit():
        text = form.text_input.data
        pass

    return render_template('chat.html', messages=messages, form=form)


'''@app.route('/predict', methods=['POST'])
def predict():
    model = tf.keras.models.load_model("model/model.keras")
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            img_bytes = image.read()
            img_data = io.BytesIO(img_bytes)

            img = tf.keras.preprocessing.image.load_img(img_data, target_size=(128, 128))
            input_array = tf.keras.preprocessing.image.img_to_array(img)  # Use loaded image 'img' here
            input_array = np.expand_dims(input_array, axis=0)  # Expand dimensions to match model input shape

            prediction = model.predict(input_array)

            result_index = np.argmax(prediction)

            class_name = ['Apple___Apple_scab',
                        'Apple___Black_rot',
                        'Apple___Cedar_apple_rust',
                        'Apple___healthy',
                        'Blueberry___healthy',
                        'Cherry_(including_sour)___Powdery_mildew',
                        'Cherry_(including_sour)___healthy',
                        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                        'Corn_(maize)___Common_rust_',
                        'Corn_(maize)___Northern_Leaf_Blight',
                        'Corn_(maize)___healthy',
                        'Grape___Black_rot',
                        'Grape___Esca_(Black_Measles)',
                        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                        'Grape___healthy',
                        'Orange___Haunglongbing_(Citrus_greening)',
                        'Peach___Bacterial_spot',
                        'Peach___healthy',
                        'Pepper,_bell___Bacterial_spot',
                        'Pepper,_bell___healthy',
                        'Potato___Early_blight',
                        'Potato___Late_blight',
                        'Potato___healthy',
                        'Raspberry___healthy',
                        'Soybean___healthy',
                        'Squash___Powdery_mildew',
                        'Strawberry___Leaf_scorch',
                        'Strawberry___healthy',
                        'Tomato___Bacterial_spot',
                        'Tomato___Early_blight',
                        'Tomato___Late_blight',
                        'Tomato___Leaf_Mold',
                        'Tomato___Septoria_leaf_spot',
                        'Tomato___Spider_mites Two-spotted_spider_mite',
                        'Tomato___Target_Spot',
                        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                        'Tomato___Tomato_mosaic_virus',
                        'Tomato___healthy']

            model_prediction = class_name[result_index]

            model_prediction = model_prediction.split('___')

            plant_name = model_prediction[0]
            disease_name = model_prediction[1]
            disease_name = disease_name.split('_')
            disease_name = " ".join(disease_name)

            img_data.seek(0)
            encoded_img = base64.b64encode(img_data.read()).decode()

            return render_template('home.html', plant_name=plant_name, disease_name=disease_name, encoded_img=encoded_img)
    return redirect(url_for('home'))'''


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
