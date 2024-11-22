import os
from flask import Flask, render_template, request, redirect, url_for, flash
from groq import Groq
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re
from collections import Counter
import string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.String(500), nullable=False)
    
    def __init__(self, prompt_text):
        self.prompt_text = prompt_text

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 30-minute session timeout
login_manager.session_protection = "strong"

# Validate password
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# Initialize Groq client



os.environ["GROQ_API_KEY"] = "your_api_key_here"
client = Groq()  # Now, it will automatically pick up the API key from the environment variable


# Route to handle prompt input and Llama response
@app.route('/prompt', methods=['GET', 'POST'])
@login_required
def prompt():
    if request.method == 'POST':
        weight = request.form['weight']
        height_feet = request.form['height_feet']
        height_inches = request.form['height_inches']
        age = request.form['age']
        gender = request.form['gender']
        health_issue = request.form['health_issue']

        # Create a prompt text for the model
        prompt_text = f"You are an expert yoga instructor and wellness advisor. Suggest yoga poses and practices suitable for an individual based on the following details Weight = {weight}kg, Height = {height_feet}ft {height_inches}in, Age = {age} years, Gender = {gender}, Health Issue = {health_issue}. Analyze whether the height and weight are appropriate for the age and provide feedback (e.g., height is less/more, weight is less/more). Suggest up to 3-5 yoga poses suitable for the individual, tailored to their health concerns and fitness goals. Include brief benefits, instructions, and precautions for each suggestion and not extend lines more than 5 and dark the yoga and dark the yoga poses"
        # Interact with Llama model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model="llama3-8b-8192",
        )

        # Extract the response from the model
        roast_text = chat_completion.choices[0].message.content

        return render_template('prompt.html', roast_text=roast_text)
    
    return render_template('prompt.html')

# Other routes remain unchanged
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate the password
        validation_error = validate_password(password)
        if validation_error:
            flash(validation_error, 'error')
            return redirect(url_for('signup'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already in use.', 'error')
            return redirect(url_for('signup'))

        # Create a new user with hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/ourTeam')
def ourTeam():
    return render_template('ourTeam.html')

@app.route('/requirements')
def requirements():
    return render_template('requirements.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pose')
def pose():
    return render_template('pose.html')  # Serve the index.html page


if __name__ == "__main__":
    app.run(port=5008)
