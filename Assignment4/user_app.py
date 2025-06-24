import json
import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
import requests
import rsa_utils
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Directory for storing student-generated PDFs
tEMP_DIR = 'pdfs'
os.makedirs(tEMP_DIR, exist_ok=True)

# File for local student database
STUDENT_DB = 'student_db.json'

# University service base URL
UNIVERSITY_API_BASE = 'http://localhost:5000'

def generate_pdf(document, signature, doc_type, roll):
    """
    Create a PDF of `document` + `signature`, save under pdfs/, and return filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{doc_type}_{roll}_{timestamp}.pdf"
    path = os.path.join(tEMP_DIR, fname)

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    title = "Grade Report" if doc_type == "grades" else "Degree Certificate"
    c.drawString(50, height - 50, title)

    c.setFont("Helvetica", 12)
    y = height - 100
    for key, val in document.items():
        c.drawString(50, y, f"{key.title()}: {val}")
        y -= 20

    # Signature section
    y -= 10
    c.drawString(50, y, "University Signature:")
    y -= 20
    c.setFont("Courier", 8)
    sig_str = ",".join(map(str, signature))
    for i in range(0, len(sig_str), 80):
        c.drawString(50, y, sig_str[i:i+80])
        y -= 12

    c.save()
    return fname

@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(tEMP_DIR, filename, as_attachment=True)

class StudentServer:
    def __init__(self):
        # Load or bootstrap the local student database
        if not os.path.exists(STUDENT_DB):
            self.db = {'students': {}}
            self.save()
        else:
            with open(STUDENT_DB, 'r') as f:
                self.db = json.load(f)
        # ensure structure
        self.db.setdefault('students', {})

        self.university_public_key = None
        self.current_student = None

    def save(self):
        with open(STUDENT_DB, 'w') as f:
            json.dump(self.db, f, indent=2)

    def register_student(self, name, roll, pwd):
        if roll in self.db['students']:
            return False, "Student already registered"

        # generate local RSA keypair
        p = rsa_utils.generate_prime(100, 1000)
        q = rsa_utils.generate_prime(100, 1000)
        pub, priv = rsa_utils.generate_keypair(p, q)

        # store student locally
        self.db['students'][roll] = {
            'name': name,
            'password': pwd,
            'public_key': pub,
            'private_key': priv
        }
        self.save()
        return True, pub

    def login(self, roll, pwd):
        # authenticate against local student DB
        student = self.db['students'].get(roll)
        if student and student['password'] == pwd:
            self.current_student = roll
            return True
        return False

student_server = StudentServer()

def _do_request(path, roll):
    # encrypt the roll using the university's public key
    payload = json.dumps({'roll': roll})
    uni_e, uni_n = student_server.university_public_key
    encrypted = rsa_utils.encrypt((uni_e, uni_n), payload)

    # call the university service
    url = f"{UNIVERSITY_API_BASE}/api/{path}"
    resp = requests.post(url, json={'encrypted_data': encrypted}, timeout=5)
    resp.raise_for_status()
    res = resp.json()

    if 'error' in res:
        return None, False, None

    serialized = json.dumps(res['document'], sort_keys=True, separators=(',', ':'))
    valid = rsa_utils.verify_signature((uni_e, uni_n), serialized, res['signature'])

    pdf_name = generate_pdf(res['document'], res['signature'], path, roll)
    return res['document'], valid, pdf_name

@app.route('/')
def home():
    return render_template('student_login.html')

@app.route('/login', methods=['POST'])
def login():
    roll = request.form['roll']
    pwd  = request.form['password']
    if not student_server.login(roll, pwd):
        return "Invalid credentials", 401

    # fetch uni public key once on successful login
    try:
        resp = requests.get(f"{UNIVERSITY_API_BASE}/api/public_key", timeout=3)
        resp.raise_for_status()
        student_server.university_public_key = resp.json()['public_key']
    except requests.exceptions.RequestException as e:
        app.logger.error("Cannot reach University service: %s", e)
        return "University service unavailable.", 503

    name = student_server.db['students'][roll]['name']
    return render_template('student_dashboard.html', roll=roll, name=name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        pwd  = request.form['password']

        ok, pub = student_server.register_student(name, roll, pwd)
        if not ok:
            return render_template('student_register.html', error=pub)

        # register with university
        # fetch latest uni key
        student_server.university_public_key = requests.get(
            f"{UNIVERSITY_API_BASE}/api/public_key"
        ).json()['public_key']

        enc = rsa_utils.encrypt(
            (student_server.university_public_key[0], student_server.university_public_key[1]),
            json.dumps({'name': name, 'roll': roll, 'password': pwd, 'public_key': pub})
        )
        uni_resp = requests.post(
            f"{UNIVERSITY_API_BASE}/api/register",
            json={'encrypted_data': enc},
            timeout=5
        )
        uni_resp.raise_for_status()
        resp = uni_resp.json()

        if resp.get('success'):
            return render_template('student_login.html', message="Registration successful. Please login.")
        return render_template('student_register.html', error="University refused")

    return render_template('student_register.html')

@app.route('/request_grades', methods=['POST'])
def request_grades():
    roll = request.form['roll']
    doc, valid, pdf = _do_request('request_grades', roll)
    return render_template('student_grades.html', document=doc, signature_valid=valid, pdf_filename=pdf)

@app.route('/request_degree', methods=['POST'])
def request_degree():
    roll = request.form['roll']
    doc, valid, pdf = _do_request('request_degree', roll)
    return render_template('student_degree.html', document=doc, signature_valid=valid, pdf_filename=pdf)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
