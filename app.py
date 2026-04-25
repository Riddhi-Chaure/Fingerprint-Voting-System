import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import CSRFProtect
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import webbrowser
import threading


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is not set in .env")

csrf = CSRFProtect(app)

#Initialize Firebase
key_file = os.environ.get('FIREBASE_KEY_PATH', 'serviceAccountKey.json')

try:
    cred = credentials.Certificate(key_file)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase with {key_file}. {e}")
    db = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not db:
        return "Database not initialized. Check server logs.", 500

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        fingerprint_id = request.form.get('fingerprint_id', '').strip()

        # ── Server-side validation ──
        if not student_id or not name or not fingerprint_id:
            return render_template('register.html', message='All fields are required', message_type='error')

        user_ref = db.collection('users').document(student_id)
        if user_ref.get().exists:
            return render_template('register.html', message='User already exists', message_type='error')
        
        user_ref.set({
            'name': name,
            'fingerprint_id': fingerprint_id,
            'has_voted': False
        })
        
        return render_template('register.html', message='User Registered Successfully', message_type='success')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not db:
        return "Database not initialized. Check server logs.", 500

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        fingerprint_id = request.form.get('fingerprint_id', '').strip()

        if not student_id or not fingerprint_id:
            return render_template('login.html', message='All fields are required')

        user_ref = db.collection('users').document(student_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            # Support both old field name ('fingerprint') and new ('fingerprint_id')
            stored_fingerprint = user_data.get('fingerprint_id') or user_data.get('fingerprint')

            if stored_fingerprint and stored_fingerprint.strip().lower() == fingerprint_id.strip().lower():
                session['student_id'] = student_id
                return redirect(url_for('vote'))
            else:
                return render_template('login.html', message='Invalid Fingerprint ID')
        else:
            return render_template('login.html', message='User not found')
            
    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if not db:
        return "Database not initialized. Check server logs.", 500

    if 'student_id' not in session:
        return redirect(url_for('login'))
        
    student_id = session['student_id']
    user_ref = db.collection('users').document(student_id)
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        session.pop('student_id', None)
        return redirect(url_for('login'))
        
    user_data = user_doc.to_dict()
    
    if request.method == 'POST':
        if user_data.get('has_voted') or user_data.get('hasVoted'):
            return render_template('vote.html', message='You have already voted', message_type='error')
            
        candidate = request.form.get('candidate', '').strip()

        allowed_candidates = ['Candidate A', 'Candidate B']
        if candidate not in allowed_candidates:
            return render_template('vote.html', message='Invalid candidate selection', message_type='error')
            
        db.collection('votes').document(student_id).set({
            'candidate': candidate
        })
        
        user_ref.update({'has_voted': True})
        
        return render_template('vote.html', message='Vote Cast Successfully', message_type='success')
        
    if user_data.get('has_voted') or user_data.get('hasVoted'):
        return render_template('vote.html', message='You have already voted', message_type='error')
        
    return render_template('vote.html')

@app.route('/results')
def results():
    if not db:
        return "Database not initialized. Check server logs.", 500

    if 'student_id' not in session:
        return redirect(url_for('login'))

    votes_ref = db.collection('votes')
    votes = [doc.to_dict() for doc in votes_ref.stream()]
    
    votes_a = sum(1 for v in votes if v.get('candidate') == 'Candidate A')
    votes_b = sum(1 for v in votes if v.get('candidate') == 'Candidate B')
    
    total_votes = votes_a + votes_b
    
    percent_a = int(votes_a / total_votes * 100) if total_votes > 0 else 0
    percent_b = int(votes_b / total_votes * 100) if total_votes > 0 else 0
    
    return render_template('results.html', 
                          votes_a=votes_a, percent_a=percent_a,
                          votes_b=votes_b, percent_b=percent_b)

@app.route('/logout')
def logout():
    session.pop('student_id', None)
    return redirect(url_for('index'))

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, open_browser).start()
    app.run(debug=debug_mode)
