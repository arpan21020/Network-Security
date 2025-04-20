
import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import rsa_utils
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

app = Flask(__name__)

# ensure the folder for PDFs exists
PDF_DIR = os.path.join(app.static_folder, 'certificates')
os.makedirs(PDF_DIR, exist_ok=True)

def create_signed_pdf(document: dict, signature, roll: str, doc_type: str) -> str:
    """
    Renders a PDF for `document` (grades or degree), embeds the `signature` as text,
    saves it under static/certificates/, and returns the relative path.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{doc_type}_{roll}_{timestamp}.pdf"
    path = os.path.join(PDF_DIR, filename)

    c = canvas.Canvas(path, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 18)
    title = "Grade Report" if doc_type=="grades" else "Degree Certificate"
    c.drawString(72, 750, title)

    c.setFont("Helvetica", 12)
    y = 720
    for key, val in document.items():
        c.drawString(72, y, f"{key.capitalize()}: {val}")
        y -= 20

    # leave some space, then embed signature
    y -= 20
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(72, y, f"Signature: {signature}")

    c.showPage()
    c.save()

    # return path relative to static folder
    return f"certificates/{filename}"

class UniversityServer:
    def __init__(self):
        self.load_database()
        if not self.db['university']['public_key']:
            self.generate_university_keys()

    def load_database(self):
        with open('database.json','r') as f:
            self.db = json.load(f)

    def save_database(self):
        with open('database.json','w') as f:
            json.dump(self.db, f, indent=2)
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

    def generate_university_keys(self):
        p = rsa_utils.generate_prime(100,1000)
        q = rsa_utils.generate_prime(100,1000)
        public_key, private_key = rsa_utils.generate_keypair(p,q)
        self.db['university']['public_key']  = public_key
        self.db['university']['private_key'] = private_key
        self.save_database()

    def get_student_data(self, roll):
        return self.db['university']['students'].get(roll)

    def generate_signed_document(self, roll):
        student = self.get_student_data(roll)
        if not student:
            return None

        doc = {
            'name': student['name'],
            'roll': roll,
            'grades': student['grades'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        serialized = json.dumps(doc, sort_keys=True, separators=(',',':'))
        sig = rsa_utils.sign(self.db['university']['private_key'], serialized)

        pdf_path = create_signed_pdf(doc, sig, roll, doc_type="grades")
        return {'document': doc, 'signature': sig, 'pdf_path': pdf_path}

    def generate_signed_degree(self, roll):
        student = self.get_student_data(roll)
        if not student:
            return None

        doc = {
            'name': student['name'],
            'roll': roll,
            'degree': 'Bachelor of Technology',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        serialized = json.dumps(doc, sort_keys=True, separators=(',',':'))
        sig = rsa_utils.sign(self.db['university']['private_key'], serialized)

        pdf_path = create_signed_pdf(doc, sig, roll, doc_type="degree")
        return {'document': doc, 'signature': sig, 'pdf_path': pdf_path}

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
    enc = request.json['encrypted_data']
    priv = university.db['university']['private_key']
    decrypted = rsa_utils.decrypt((priv[0],priv[1]), enc)
    roll = json.loads(decrypted)['roll']

    signed = university.generate_signed_document(roll)
    return jsonify(signed) if signed else (jsonify({'error':'Not found'}),404)

@app.route('/api/request_degree', methods=['POST'])
def request_degree():
    enc = request.json['encrypted_data']
    priv = university.db['university']['private_key']
    decrypted = rsa_utils.decrypt((priv[0],priv[1]), enc)
    roll = json.loads(decrypted)['roll']

    signed = university.generate_signed_degree(roll)
    return jsonify(signed) if signed else (jsonify({'error':'Not found'}),404)

# ... other endpoints unchanged ...

if __name__=='__main__':
    app.run(port=5000, debug=True)
