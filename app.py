from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

if not os.path.exists('data'):
    os.makedirs('data')

@contextmanager
def get_json(filename):
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    yield data
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Define index route (used in logout redirect)
@app.route('/')
def index():
    return '<h1>Welcome to Key Locker</h1><p><a href="/login">Login</a> | <a href="/register">Register</a></p>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation checks
        if not username or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long!', 'error')
            return redirect(url_for('register'))
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        # Check if username already exists
        with get_json('users.json') as users:
            if username in users:
                flash('Username already exists! Please choose a different username.', 'error')
                return redirect(url_for('register'))
            
            # Create new user
            users[username] = {
                'password_hash': generate_password_hash(password),
                'created_at': datetime.utcnow().isoformat()
            }
            
            flash('Registration successful! Please login with your credentials.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_json('users.json') as users:
            user = users.get(username)
            if user and check_password_hash(user['password_hash'], password):
                session['username'] = username
                flash('Login successful.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    username = session['username']
    with get_json('keys.json') as all_keys:
        user_keys = all_keys.get(username, [])
    return render_template('dashboard.html', keys=user_keys, username=username)

@app.route('/add_key', methods=['POST'])
def add_key():
    if 'username' not in session:
        flash('Please log in to add keys.', 'error')
        return redirect(url_for('login'))
    key_name = request.form['key_name']
    key_value = request.form['key_value']
    key_desc = request.form.get('key_description', '')
    if not key_name or not key_value:
        flash('Key name and value are required.', 'error')
        return redirect(url_for('dashboard'))
    username = session['username']
    with get_json('keys.json') as all_keys:
        user_keys = all_keys.setdefault(username, [])
        # Optionally check for duplicates here
        user_keys.append({
            'name': key_name,
            'value': key_value,
            'description': key_desc,
            'created_at': datetime.utcnow().isoformat()
        })
    flash('Key added successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_key/<key_name>')
def delete_key(key_name):
    if 'username' not in session:
        flash('Please log in to delete keys.', 'error')
        return redirect(url_for('login'))
    username = session['username']
    with get_json('keys.json') as all_keys:
        user_keys = all_keys.get(username, [])
        all_keys[username] = [k for k in user_keys if k['name'] != key_name]
    flash('Key deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
