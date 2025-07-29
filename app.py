from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_current_streak(self):
        return 0

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("=== LOGIN ROUTE ACCESSED ===")
    if request.method == 'GET':
        print("GET request - rendering login template")
        try:
            if '_flashes' in session and 'Logged out successfully' in [msg[1] for msg in session.get('_flashes', [])]:
                logout_user()
                session.clear()
                print("Forced logout due to post-logout redirect")
            elif current_user.is_authenticated:
                print("User already authenticated, redirecting to habits")
                return redirect(url_for('habits'))
            template_path = os.path.join(app.template_folder, 'login.html')
            if not os.path.exists(template_path):
                print("Login template not found")
                flash('Login page unavailable', 'error')
                return render_template('error.html', message='Login page not found')
            return render_template('login.html')
        except Exception as e:
            print(f"Error rendering login template: {e}")
            import traceback
            print(traceback.format_exc())
            flash(f"Error loading login page: {str(e)}", 'error')
            return render_template('error.html', message='Error loading login page')

    print("POST request - processing login")
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        print(f"Username: '{username}'")
        print(f"Password received: {'Yes' if password else 'No'}")
        if not username or not password:
            print("Missing username or password")
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        print(f"Looking for user: {username}")
        user = User.query.filter_by(username=username).first()
        if not user:
            print("User not found")
            flash('User not found', 'error')
            return render_template('login.html')
        print(f"User found: {user.username}")
        print("Checking password...")
        if bcrypt.check_password_hash(user.password, password):
            print("Password correct - logging in user")
            login_user(user, remember=True)
            print("User logged in successfully")
            flash('Login successful!', 'success')
            return redirect(url_for('habits'))
        else:
            print("Password incorrect")
            flash('Invalid password', 'error')
            return render_template('login.html')
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        import traceback
        print(traceback.format_exc())
        flash('Login failed due to server error', 'error')
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        try:
            template_path = os.path.join(app.template_folder, 'register.html')
            if not os.path.exists(template_path):
                print("Register template not found")
                flash('Registration page unavailable', 'error')
                return render_template('error.html', message='Registration page not found')
            return render_template('register.html')
        except Exception as e:
            print(f"Error rendering register template: {e}")
            flash(f"Error loading registration page: {str(e)}", 'error')
            return render_template('error.html', message='Error loading registration page')

    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        print(f"Registration: {username}, {email}")
        if not all([username, email, password]):
            flash('Please fill in all fields', 'error')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print(f"User created successfully: {username}")
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        flash('Registration failed. Please try again.', 'error')
        return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    print("=== LOGOUT ROUTE ACCESSED ===")
    try:
        logout_user()
        session.pop('_flashes', None)
        session.clear()
        from flask import make_response
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('remember_token', '', expires=0)
        flash('Logged out successfully', 'success')
        print(f"Redirecting to {url_for('login')}")
        return resp
    except Exception as e:
        print(f"LOGOUT ERROR: {e}")
        import traceback
        print(traceback.format_exc())
        flash('Logout failed due to server error', 'error')
        return redirect(url_for('login'))

@app.route('/habits', methods=['GET', 'POST'])
@login_required
def habits():
    print(f"Habits accessed by user: {current_user.username}")
    if request.method == 'POST':
        if 'delete' in request.form:
            habit_id = request.form['delete']
            habit = Habit.query.get_or_404(habit_id)
            if habit.user_id == current_user.id:
                db.session.delete(habit)
                db.session.commit()
                flash('Habit deleted successfully', 'success')
        else:
            name = request.form.get('name', '').strip()
            if name:
                habit = Habit(name=name, user_id=current_user.id)
                db.session.add(habit)
                db.session.commit()
                flash('Habit created/updated successfully', 'success')
            else:
                flash('Habit name is required', 'error')
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('habits.html', habits=habits)

@app.route('/clear-session')
def clear_session():
    session.clear()
    logout_user()
    flash('Session cleared', 'info')
    return redirect(url_for('login'))

@app.route('/debug-users')
def debug_users():
    try:
        users = User.query.all()
        user_info = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password_hash_length': len(user.password)
            }
            for user in users
        ]
        return jsonify(user_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

with app.app_context():
    db.create_all()
    print("Database initialized")

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)