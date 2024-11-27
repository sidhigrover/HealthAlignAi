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
os.environ["GROQ_API_KEY"] = "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"
client = Groq()  

def format_model_output(response_text):
    formatted_output = []
    lines = response_text.split('\n')
    is_in_list = False

    for line in lines:
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            if not is_in_list:
                formatted_output.append("<ul>")
                is_in_list = True
            formatted_output.append(f"<li>{line[2:].strip()}</li>")  # Add the bullet point
        else:
            if is_in_list:
                formatted_output.append("</ul>")
                is_in_list = False
            formatted_output.append(line)  # Add plain text as-is

    # Close any unclosed list
    if is_in_list:
        formatted_output.append("</ul>")

    return "<br>".join(formatted_output)  # Join everything with line breaks for HTML

# Route to handle input and response
@app.route('/prompt', methods=['GET', 'POST'])
@login_required
def prompt():
    if request.method == 'POST':
        # Collect user input
        weight = request.form['weight']
        height_feet = request.form['height_feet']
        height_inches = request.form['height_inches']
        age = request.form['age']
        gender = request.form['gender']
        health_issue = request.form['health_issue']

        # Create a prompt for the AI model
        prompt_text = (
            f"You are an expert yoga instructor and wellness advisor. Based on the following details:\n"
            f"- Weight: {weight}kg\n"
            f"- Height: {height_feet}ft {height_inches}in\n"
            f"- Age: {age} years\n"
            f"- Gender: {gender}\n"
            f"- Health Issue: {health_issue}\n\n"
            f"Provide a structured response with:\n"
            f"1. Height and weight analysis.\n"
            f"2. 3-5 yoga poses, each with benefits, instructions, and precautions.\n"
            f"Each point must start with '- ' or '* ' and be concise."
        )

        # Call the AI model for completion
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model="llama3-8b-8192",
        )

        # Get the model's raw response
        response_text = chat_completion.choices[0].message.content

        # Format response for HTML
        formatted_text = format_model_output(response_text)

        # Render response in the template
        return render_template('prompt.html', formatted_text=formatted_text)

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



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pose')
def pose():
    return render_template('pose.html')  

@app.route('/video_feed')
def video_feed():
    return Response(pose_detection.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream video frames



if __name__ == "__main__":
    app.run(port=5092)
