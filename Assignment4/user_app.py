
# user_app.py
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
import requests
import rsa_utils

# PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

PDF_DIR = 'pdfs'
os.makedirs(PDF_DIR, exist_ok=True)

def generate_pdf(document, signature, doc_type, roll):
    """
    Create a PDF of `document` + `signature`, save under pdfs/, and return filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{doc_type}_{roll}_{timestamp}.pdf"
    path = os.path.join(PDF_DIR, fname)

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    title = "Grade Report" if doc_type=="grades" else "Degree Certificate"
    c.drawString(50, height - 50, title)

    c.setFont("Helvetica", 12)
    y = height - 100
    for key, val in document.items():
        c.drawString(50, y, f"{key.title()}: {val}")
        y -= 20

    # leave a bit of space, then draw signature
    y -= 10
    c.drawString(50, y, "University Signature:")
    y -= 20
    c.setFont("Courier", 8)
    sig_str = ",".join(map(str, signature))
    # wrap signature lines at ~80 chars
    for i in range(0, len(sig_str), 80):
        c.drawString(50, y, sig_str[i:i+80])
        y -= 12

    c.save()
    return fname

@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename, as_attachment=True)

class StudentServer:
    def __init__(self):
        with open('database.json','r') as f:
            self.db = json.load(f)
        self.university_public_key = None
        self.current_student = None

    def save(self):
        with open('database.json','w') as f:
            json.dump(self.db, f, indent=2)

    def register_student(self, name, roll, pwd):
        if roll in self.db['students']:
            return False, "Student already registered"
        p = rsa_utils.generate_prime(100,1000)
        q = rsa_utils.generate_prime(100,1000)
        pub, priv = rsa_utils.generate_keypair(p,q)
        self.db['students'][roll] = {
            'name': name,
            'password': pwd,
            'public_key': pub,
            'private_key': priv
        }
        self.save()
        return True, pub

    def login(self, roll, pwd):
        
        s = self.db['university']['students'].get(roll)
        if s and s['password']==pwd:
            self.current_student = roll
            return True
        return False

student_server = StudentServer()

def _do_request(path, roll):
    # encrypt the roll
    payload = json.dumps({'roll':roll})
    uni_e, uni_n = student_server.university_public_key
    encrypted = rsa_utils.encrypt((uni_e, uni_n), payload)

    # call university
    res = requests.post(
        f'http://localhost:5000/api/{path}',
        json={'encrypted_data': encrypted}
    ).json()

    if 'error' in res:
        return None, False, None

    # verify JSON signature
    serialized = json.dumps(res['document'], sort_keys=True, separators=(',',':'))
    valid = rsa_utils.verify_signature(
        (uni_e, uni_n),
        serialized,
        res['signature']
    )

    # generate PDF
    pdf_name = generate_pdf(res['document'], res['signature'], path, roll)
    return res['document'], valid, pdf_name

@app.route('/')
def home():
    return render_template('student_login.html')

@app.route('/login', methods=['POST'])
def login():
    roll = request.form['roll']
    pwd  = request.form['password']
    if student_server.login(roll, pwd):
        # fetch uni public key once on login
        student_server.university_public_key = requests.get(
            'http://localhost:5000/api/public_key'
        ).json()['public_key']
        return render_template('student_dashboard.html', roll=roll,name=student_server.db['university']['students'][roll]['name'])
    return "Invalid credentials", 401

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name = request.form['name']
        roll = request.form['roll']
        pwd  = request.form['password']
        ok, pub = student_server.register_student(name, roll, pwd)
        if not ok:
            return render_template('student_register.html', error=pub)
        # get uni pub key
        student_server.university_public_key = requests.get(
            'http://localhost:5000/api/public_key'
        ).json()['public_key']
        # send registration
        enc = rsa_utils.encrypt(
            (student_server.university_public_key[0],
             student_server.university_public_key[1]),
            json.dumps({'name':name,'roll':roll,'password':pwd,'public_key':pub})
        )
        resp = requests.post(
            'http://localhost:5000/api/register',
            json={'encrypted_data':enc}
        ).json()
        if resp.get('success'):
            return render_template('student_login.html',
                                   message="Registration successful. Please login.")
        return render_template('student_register.html', error="University refused")
    return render_template('student_register.html')

@app.route('/request_grades', methods=['POST'])
def request_grades():
    roll = request.form['roll']
    doc, valid, pdf = _do_request('request_grades', roll)
    return render_template('student_grades.html',
                           document=doc,
                           signature_valid=valid,
                           pdf_filename=pdf)

@app.route('/request_degree', methods=['POST'])
def request_degree():
    roll = request.form['roll']
    doc, valid, pdf = _do_request('request_degree', roll)
    return render_template('student_degree.html',
                           document=doc,
                           signature_valid=valid,
                           pdf_filename=pdf)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
