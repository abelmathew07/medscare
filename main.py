from flask import Flask, render_template, request, redirect, url_for, jsonify,send_file 
from sqlalchemy.exc import IntegrityError
from flask_restful import Api 
from flask_sqlalchemy import SQLAlchemy
from gen_op import GenerateOPTicket
from model import predict
import json
import requests
from datetime import datetime

import random

random_number = random.randint(10000, 99999)

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class HealthDatas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
class Userdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_user():
    try:
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('error.html', error='Username already exists!')
        
        # If the username doesn't exist, create a new user and add it to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html')
    
    except IntegrityError:
        # Handle any IntegrityError, such as violating unique constraint
        db.session.rollback()  # Rollback any changes made to the session
        return render_template('index.html', error='IntegrityError occurred!')
    # except Exception as e:
    #     # Handle any potential errors here
    #     return render_template('error.html', error=str(e))

@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

@app.route('/homes')
def homes():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/health-data', methods=['POST'])
def submit_health_data():
    # Get data from request
    data = request.get_json()
    heart_rate = data.get('heart_rate')
    spo2 = data.get('spo2')
    temperature = data.get('temperature')
    
    # Validate data
    if heart_rate is None or spo2 is None or temperature is None:
        return jsonify({'error': 'Missing data parameters'}), 400
    
    # Create a new HealthData object and add it to the database
    new_data = HealthDatas(heart_rate=heart_rate, spo2=spo2, temperature=temperature)
    db.session.add(new_data)
    db.session.commit()
    
    return jsonify({'message': 'Health data submitted successfully'}), 201

def get_last_health_data():
    last_data = HealthDatas.query.order_by(HealthDatas.timestamp.desc()).first()
    return last_data

@app.route('/process', methods=['POST'])
def process():
    symptoms_string = request.form['symptoms']
    print(symptoms_string)
    last_data = get_last_health_data()
    print(last_data)
    symptoms_list = symptoms_string.split(',')
    disease=predict(symptoms_list)
    
    comma_separated_string = ', '.join(disease)
    random_number = random.randint(10000, 99999)
    hr = random.randint(60, 90)
    print(comma_separated_string) 
    data = {
        "patient_name": request.form['name'],
        "Age": request.form['age'],
        "Gender": request.form['gender'],
        "id":random_number,
        "hr":last_data.heart_rate,
        "spo2": last_data.spo2,
       "temperature": last_data.temperature,
        "address": request.form['address'],
        "Phone Number": request.form['number'],
        "Department": request.form['dept'],
        "Medical Insurance": request.form['Insurance'],
        "symptoms": request.form['symptoms'],
        "predicted_disease": comma_separated_string
    }

    json_data = json.dumps(data, indent=4)
    opticket_generator = GenerateOPTicket()
    pdf_data = opticket_generator.generate_pdf(data)

    if pdf_data:
        with open("opticket.pdf", "wb") as f:
            f.write(pdf_data)
        return redirect(url_for('open_pdf'))
    else:
        print("Failed to generate PDF.")
        return render_template('home.html')

@app.route('/open_pdf')
def open_pdf():
    pdf_path = 'opticket.pdf'  # Path to your PDF file
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)




