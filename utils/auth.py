import json
import hashlib
import os
import streamlit as st

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

def _ensure_data_dir():
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

def _load_users():
    _ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users):
    _ensure_data_dir()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password, college='', domain='Data Science', year=''):
    users = _load_users()
    email = email.lower().strip()
    if email in users:
        return False, "Email already registered! Please login."
    users[email] = {
        'name': name,
        'email': email,
        'password': _hash_password(password),
        'college': college,
        'domain': domain,
        'year': year,
        'skills': [],
        'resume_text': '',
        'resume_score': 0,
        'job_match': 0,
        'exams_taken': 0,
        'highest_score': 0,
        'assignments': 0,
    }
    _save_users(users)
    return True, "Account created successfully!"

def login_user(email, password):
    users = _load_users()
    email = email.lower().strip()
    if email not in users:
        return False, None
    user = users[email]
    if user['password'] != _hash_password(password):
        return False, None
    return True, user

def update_user(email, updates: dict):
    users = _load_users()
    email = email.lower().strip()
    if email in users:
        users[email].update(updates)
        _save_users(users)
        # Update session state too
        if 'user' in st.session_state:
            st.session_state['user'].update(updates)

def check_auth():
    return st.session_state.get('logged_in', False)

def get_current_user():
    return st.session_state.get('user', None)

def logout():
    for key in ['logged_in', 'user', 'email', 'current_page',
                'resume_text', 'extracted_skills', 'analysis_done',
                'exam_submitted', 'exam_answers', 'exam_score']:
        if key in st.session_state:
            del st.session_state[key]
