from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Blog model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('index.html', blogs=blogs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/add_blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        author = request.form['author']
        email = request.form['email']
        phone = request.form['phone']
        title = request.form['title']
        content = request.form['content']

        new_blog = Blog(
            author=author,
            email=email,
            phone=phone,
            title=title,
            content=content
        )

        try:
            db.session.add(new_blog)
            db.session.commit()
            flash("✅ Blog added successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"❌ Error: {str(e)}", "danger")
            return redirect(url_for('add_blog'))

    return render_template('add_blog.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            flash("✅ Account created. Please log in.", "success")
            return redirect(url_for('login'))
        except:
            flash("❌ Username or Email already exists.", "danger")
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Logged in successfully.", "success")
            return redirect(url_for('index'))
        else:
            flash("❌ Invalid credentials.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("🔒 Logged out.", "info")
    return redirect(url_for('index'))

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
