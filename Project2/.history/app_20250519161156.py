from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey"  # Required for flashing messages

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Blog model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Blog {self.title}>'

# Home page
@app.route('/')
def index():
    blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('index.html', blogs=blogs)

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Help page
@app.route('/help')
def help():
    return render_template('help.html')

# Add blog page
@app.route('/add_blog', methods=['GET', 'POST'])
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

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
