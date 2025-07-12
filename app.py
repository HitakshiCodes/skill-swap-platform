from flask import Flask, render_template, request, redirect
from database import engine, Base
from model.user import User

app = Flask(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        return render_template("dashboard.html", name=name)
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", name="Test User")

if __name__ == '__main__':
    app.run(debug=True)

