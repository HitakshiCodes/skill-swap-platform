from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = 'your-secret-key'

init_db()

# 🔐 Register route
@app.route("/add", methods=["POST"])
def add_skill():
    name = request.form["name"]
    contact = request.form["contact"]
    offer = request.form["offer"]
    want = request.form["want"]
    availability = request.form["availability"]
    is_public = 1 if "is_public" in request.form else 0

    with sqlite3.connect("skill_swap.db") as conn:
        conn.execute("""
            INSERT INTO skills (name, contact, offer, want, availability, is_public)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, contact, offer, want, availability, is_public))

    return redirect(url_for("index"))


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
def submit_skill():   # <-- renamed from add_skill
    # your logic here

    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        want = request.form['want']
        contact = request.form['contact']
        location = request.form['location']
        mode = request.form['mode']
        with sqlite3.connect("skill_swap.db") as conn:
            conn.execute("""
                INSERT INTO skills (name, skill, want, contact, location, mode)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, skill, want, contact, location, mode))
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




