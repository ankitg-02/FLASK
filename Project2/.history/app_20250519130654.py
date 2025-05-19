from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
blogs = []
@app.route('/')
def index():
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
def add_blog():
    if request.method == 'POST':
        # Get data from form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        content = request.form.get('content')

        # Save the blog entry
        blogs.append({
            'name': name,
            'email': email,
            'phone': phone,
            'content': content
        })

        return redirect(url_for('index'))

    return render_template('add_blog.html')
if __name__ == '__main__':
    app.run(debug=True)
