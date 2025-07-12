from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = 'your-secret-key'

init_db()

# 🔐 Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect("skill_swap.db") as conn:
            try:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash('Registration successful. Please log in.')
                return redirect('/login')
            except sqlite3.IntegrityError:
                flash('Username already exists.')
    return render_template('register.html')

# 🔐 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect("skill_swap.db") as conn:
            user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
            if user:
                session['user'] = username
                return redirect('/')
            else:
                flash('Invalid credentials.')
    return render_template('login.html')

# 🔓 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')

# ➕ Add Skill
@app.route('/add-skill', methods=['GET', 'POST'])
def add_skill():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        want = request.form['want']
        with sqlite3.connect("skill_swap.db") as conn:
            conn.execute("INSERT INTO skills (name, skill, want) VALUES (?, ?, ?)", (name, skill, want))
            conn.commit()
        return redirect('/dashboard')
    return render_template('add-skill.html')

# 📋 Dashboard
@app.route('/dashboard')
def dashboard():
    with sqlite3.connect("skill_swap.db") as conn:
        conn.row_factory = sqlite3.Row  # 👈 this line makes it return dict-like rows
        skills = conn.execute("SELECT * FROM skills").fetchall()
    return render_template('dashboard.html', skills=skills)

if __name__ == '__main__':
    app.run(debug=True)




