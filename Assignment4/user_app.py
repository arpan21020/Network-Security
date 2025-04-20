import json
import random
from flask import Flask, render_template, request, jsonify
import requests
import rsa_utils

app = Flask(__name__)

class StudentServer:
    def __init__(self):
        self.load_database()
        self.university_public_key = None
        self.current_student = None
    
    def load_database(self):
        with open('database.json', 'r') as f:
            self.db = json.load(f)
    
    def save_database(self):
        with open('database.json', 'w') as f:
            json.dump(self.db, f, indent=2)
    
    def register_student(self, name, roll, password):
        if roll in self.db['students']:
            return False, "Student already registered"
        
        p = rsa_utils.generate_prime(100, 1000)
        q = rsa_utils.generate_prime(100, 1000)
        public_key, private_key = rsa_utils.generate_keypair(p, q)
        
        self.db['students'][roll] = {
            'name': name,
            'password': password,
            'public_key': public_key,
            'private_key': private_key
        }
        
        self.save_database()
        return True, public_key
    
    def login(self, roll, password):
        if roll in self.db['students'] and self.db['students'][roll]['password'] == password:
            self.current_student = roll
            return True
        return False
    
    def get_student_keys(self, roll):
        if roll in self.db['students']:
            return {
                'public_key': self.db['students'][roll]['public_key'],
                'private_key': self.db['students'][roll]['private_key']
            }
        return None

student_server = StudentServer()

@app.route('/')
def home():
    return render_template('student_login.html')

@app.route('/login', methods=['POST'])
def login():
    roll = request.form.get('roll')
    password = request.form.get('password')
    
    if student_server.login(roll, password):
        return render_template('student_dashboard.html', roll=roll)
    return "Invalid credentials", 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        roll = request.form.get('roll')
        password = request.form.get('password')
        
        success, public_key = student_server.register_student(name, roll, password)
        
        if success:
            # Get university public key
            uni_pub_key = requests.get('http://localhost:5000/api/public_key').json()['public_key']
            
            # Prepare encrypted registration data
            student_data = {
                'name': name,
                'roll': roll,
                'password': password,
                'public_key': public_key
            }
            
            encrypted_data = rsa_utils.encrypt(
                (uni_pub_key[0], uni_pub_key[1]),
                json.dumps(student_data)
            )
            
            # Send registration to university
            response = requests.post('http://localhost:5000/api/register', json={
                'encrypted_data': encrypted_data
            }).json()
            
            if response['success']:
                student_server.university_public_key = response['university_public_key']
                return render_template('student_login.html', message="Registration successful. Please login.")
        
        return render_template('student_register.html', error="Registration failed")
    
    return render_template('student_register.html')

@app.route('/request_grades', methods=['POST'])
def request_grades():
    roll = request.form.get('roll')
    student_keys = student_server.get_student_keys(roll)
    
    if not student_keys:
        return "Student not found", 404
    
    # Prepare request data
    request_data = {
        'roll': roll
    }
    
    # Encrypt with university public key
    encrypted_data = rsa_utils.encrypt(
        (student_server.university_public_key[0], student_server.university_public_key[1]),
        json.dumps(request_data)
    )
    
    # Send request to university
    response = requests.post('http://localhost:5000/api/request_grades', json={
        'encrypted_data': encrypted_data
    }).json()
    
    if 'error' in response:
        return response['error'], 404
    
    # Verify signature
    is_valid = rsa_utils.verify_signature(
        (student_server.university_public_key[0], student_server.university_public_key[1]),
        str(response['document']),
        response['signature']
    )
    
    if is_valid:
        return render_template('student_grades.html', 
                             document=response['document'],
                             signature_valid=True)
    else:
        return render_template('student_grades.html', 
                             document=response['document'],
                             signature_valid=False)

if __name__ == '__main__':
    app.run(port=5001,debug=True)