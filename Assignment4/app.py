import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import rsa_utils
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

app = Flask(__name__)

# Directory for storing generated PDFs
PDF_DIR = os.path.join(app.static_folder or '.', 'certificates')
# ensure the certificate folder exists
os.makedirs(PDF_DIR, exist_ok=True)

# File for the university database
UNIVERSITY_DB = 'university_db.json'

class UniversityServer:
    def __init__(self):
        self.db_file = UNIVERSITY_DB
        self.load_database()
        # generate keys if missing
        uni = self.db['university']
        if not uni.get('public_key') or not uni.get('private_key'):
            self.generate_university_keys()

    def load_database(self):
        # bootstrap or load the JSON file; handle empty or malformed files
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) == 0:
            self.db = {}
        else:
            try:
                with open(self.db_file, 'r') as f:
                    self.db = json.load(f)
            except json.JSONDecodeError:
                self.db = {}
        # ensure structure
        uni = self.db.setdefault('university', {})
        uni.setdefault('public_key', None)
        uni.setdefault('private_key', None)
        uni.setdefault('students', {})
        uni.setdefault('courses', {
            'CS101': 'Introduction to Computer Science',
            'MATH201': 'Advanced Mathematics',
            'PHYS301': 'Modern Physics',
            'ENG401': 'Technical Writing'
        })
        self.save_database()

    def save_database(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.db, f, indent=2)

    def register_student(self, student_data):
        roll = student_data['roll']
        if roll in self.db['university']['students']:
            return False, 'Student already registered'
        # assign random grades
        grades = { code: random.randint(60, 95) for code in self.db['university']['courses'] }
        self.db['university']['students'][roll] = {
            'name': student_data['name'],
            'password': student_data['password'],
            'public_key': student_data['public_key'],
            'grades': grades,
            'registered_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.save_database()
        return True, 'Registration successful'

    def generate_university_keys(self):
        p = rsa_utils.generate_prime(100, 1000)
        q = rsa_utils.generate_prime(100, 1000)
        pub, priv = rsa_utils.generate_keypair(p, q)
        uni = self.db['university']
        uni['public_key'] = pub
        uni['private_key'] = priv
        self.save_database()

    def get_student(self, roll):
        return self.db['university']['students'].get(roll)

    def create_signed_pdf(self, doc, signature, roll, doc_type):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{doc_type}_{roll}_{timestamp}.pdf"
        path = os.path.join(PDF_DIR, filename)
        c = canvas.Canvas(path, pagesize=LETTER)
        c.setFont('Helvetica-Bold', 18)
        title = 'Grade Report' if doc_type=='grades' else 'Degree Certificate'
        c.drawString(72, 750, title)
        c.setFont('Helvetica', 12)
        y = 720
        for k, v in doc.items():
            c.drawString(72, y, f"{k.title()}: {v}")
            y -= 20
        y -= 20
        c.setFont('Helvetica-Oblique', 8)
        c.drawString(72, y, f"Signature: {signature}")
        c.showPage()
        c.save()
        return f"certificates/{filename}"

    def sign_document(self, roll, doc_type):
        student = self.get_student(roll)
        if not student:
            return None
        doc = {
            'name': student['name'],
            'roll': roll,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if doc_type == 'grades':
            doc['grades'] = student['grades']
        else:
            doc['degree'] = 'Bachelor of Technology'
        serialized = json.dumps(doc, sort_keys=True, separators=(',',':'))
        sig = rsa_utils.sign(self.db['university']['private_key'], serialized)
        pdf = self.create_signed_pdf(doc, sig, roll, doc_type)
        return {'document': doc, 'signature': sig, 'pdf_path': pdf}

# instantiate the server
university = UniversityServer()

@app.route('/')
def home():
    return render_template('university_login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('university_dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    u = request.form.get('username')
    p = request.form.get('password')
    if u == 'admin' and p == 'admin123':
        return redirect(url_for('dashboard'))
    return 'Invalid credentials', 401

@app.route('/api/public_key', methods=['GET'])
def get_public_key():
    return jsonify({'public_key': university.db['university']['public_key']})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    dec = rsa_utils.decrypt(tuple(university.db['university']['private_key']), data['encrypted_data'])
    student_data = json.loads(dec)
    ok, msg = university.register_student(student_data)
    return jsonify({'success': ok, 'message': msg, 'public_key': university.db['university']['public_key']})

@app.route('/api/request_grades', methods=['POST'])
def api_request_grades():
    data = request.json
    dec = rsa_utils.decrypt(tuple(university.db['university']['private_key']), data['encrypted_data'])
    roll = json.loads(dec)['roll']
    signed = university.sign_document(roll, 'grades')
    return (jsonify(signed), 200) if signed else (jsonify({'error':'Not found'}), 404)

@app.route('/api/request_degree', methods=['POST'])
def api_request_degree():
    data = request.json
    dec = rsa_utils.decrypt(tuple(university.db['university']['private_key']), data['encrypted_data'])
    roll = json.loads(dec)['roll']
    signed = university.sign_document(roll, 'degree')
    return (jsonify(signed), 200) if signed else (jsonify({'error':'Not found'}), 404)

@app.route('/api/students', methods=['GET'])
def api_students():
    students = university.db['university']['students']
    formatted = []
    for roll, info in students.items():
        formatted.append({
            'roll': roll,
            'name': info['name'],
            'registered_on': info['registered_on']
        })
    return jsonify({'total': len(formatted), 'students': formatted})

if __name__=='__main__':
    app.run(port=5000, debug=True)
