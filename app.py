from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = 'your-secret-key'

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect("skill_swap.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                session['user'] = username
                return redirect('/dashboard')
            else:
                flash("Invalid username or password.")
    return render_template('login.html')

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        profile_pic = request.files['profile_pic']
        filename = secure_filename(profile_pic.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_pic.save(filepath)

        with sqlite3.connect("skill_swap.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, profile_pic) VALUES (?, ?, ?)",
                           (username, password, filename))
            conn.commit()
        return redirect(url_for('add_skill'))
    return render_template('register.html')


@app.route('/add-skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        want = request.form['want']
        contact = request.form['contact']
        location = request.form['location']
        mode = request.form['mode']

        with sqlite3.connect("skill_swap.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    skill TEXT,
                    want TEXT,
                    contact TEXT,
                    location TEXT,
                    mode TEXT
                )
            ''')
            cursor.execute('''
                INSERT INTO skills (name, skill, want, contact, location, mode)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, skill, want, contact, location, mode))
            conn.commit()

        return redirect(url_for('dashboard'))

    return render_template('add-skill.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
         return redirect('/login')
    with sqlite3.connect("skill_swap.db") as conn:
        conn.row_factory = sqlite3.Row
        skills = conn.execute("SELECT * FROM skills").fetchall()
    return render_template('dashboard.html', skills=skills)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    with sqlite3.connect("skill_swap.db") as conn:
        conn.row_factory = sqlite3.Row
        skill = conn.execute("SELECT * FROM skills WHERE id = ?", (user_id,)).fetchone()

    if not skill:
        return "User not found", 404

    return render_template("profile.html", skill=skill)

    if not skill:
        return "User not found", 404
    return render_template("profile.html", skill=skill)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10000)
