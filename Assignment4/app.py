import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import rsa_utils

app = Flask(__name__)

class UniversityServer:
    def __init__(self):
        self.load_database()
        if not self.db['university']['public_key']:
            self.generate_university_keys()
    
    def load_database(self):
        with open('database.json', 'r') as f:
            self.db = json.load(f)
    
    def save_database(self):
        with open('database.json', 'w') as f:
            json.dump(self.db, f, indent=2)
    
    def generate_university_keys(self):
        p = rsa_utils.generate_prime(100, 1000)
        q = rsa_utils.generate_prime(100, 1000)
        public_key, private_key = rsa_utils.generate_keypair(p, q)
        self.db['university']['public_key'] = public_key
        self.db['university']['private_key'] = private_key
        self.save_database()
    
    def register_student(self, student_data):
        name = student_data['name']
        roll = student_data['roll']
        password = student_data['password']
        public_key = student_data['public_key']
        
        if roll in self.db['university']['students']:
            return False, "Student already registered"
        
        # Generate random grades for courses
        grades = {}
        for course_code in self.db['university']['courses']:
            grades[course_code] = random.randint(60, 95)
        
        self.db['university']['students'][roll] = {
            'name': name,
            'password': password,
            'public_key': public_key,
            'grades': grades,
            'registered_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_database()
        return True, "Registration successful"
    
    def get_student_data(self, roll):
        if roll in self.db['university']['students']:
            return self.db['university']['students'][roll]
        return None
    
    def generate_signed_document(self, roll):
        student_data = self.get_student_data(roll)
        if not student_data:
            return None
        
        document = {
            'name': student_data['name'],
            'roll': roll,
            'grades': student_data['grades'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        signature = rsa_utils.sign(
            self.db['university']['private_key'],
            str(document)
        )
        
        return {
            'document': document,
            'signature': signature
        }

university = UniversityServer()

@app.route('/')
def home():
    return render_template('university_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # In a real app, you'd have proper admin credentials
    if username == 'admin' and password == 'admin123':
        return render_template('university_dashboard.html')
    return "Invalid credentials", 401

@app.route('/api/public_key', methods=['GET'])
def get_public_key():
    return jsonify({
        'public_key': university.db['university']['public_key']
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    decrypted_data = rsa_utils.decrypt(
        (university.db['university']['private_key'][0], university.db['university']['private_key'][1]),
        data['encrypted_data']
    )
    student_data = json.loads(decrypted_data)
    
    success, message = university.register_student(student_data)
    return jsonify({
        'success': success,
        'message': message,
        'university_public_key': university.db['university']['public_key']
    })

@app.route('/api/request_grades', methods=['POST'])
def request_grades():
    data = request.json
    decrypted_data = rsa_utils.decrypt(
        (university.db['university']['private_key'][0], university.db['university']['private_key'][1]),
        data['encrypted_data']
    )
    request_data = json.loads(decrypted_data)
    
    roll = request_data['roll']
    signed_doc = university.generate_signed_document(roll)
    
    if signed_doc:
        return jsonify(signed_doc)
    return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(port=5000,debug=True)