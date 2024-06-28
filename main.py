from flask import Flask, abort, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from email.mime.text import MIMEText
from urllib.parse import unquote
import requests
import os
import aiosmtplib
import asyncio
import re
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
client = mongo.cx

try:
    client.admin.command('ping')
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    flash(f"Failed to connect to MongoDB: {e}")

db = client.portfoliopage
users = db.portfolio_users

db2 = client.slidesviewer
collection_slides = db2.slides

login_manager = LoginManager(app)
login_manager.login_view = 'auth'


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({'_id': user_id})
    if user:
        return User(user['_id'], user['username'])
    return None


csrf = CSRFProtect(app)
limiter = Limiter(
    app,
    default_limits=["200 per day", "50 per hour"]
)

site_key = os.environ.get('S_KEY')


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, AnonymousUserMixin):
            return "You don't have the permission to access the requested resource. Please contact for the slides."
        if int(current_user.id) != 1:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function


def verify_recaptcha(response):
    secret_key = os.environ.get("G_KEY")
    payload = {'secret': secret_key, 'response': response}
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success', False)


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def sanitize_input(user_input):
    return html.escape(user_input.strip())


async def send_email_async(message, receiver_email):
    my_email = os.environ.get("E_ID")
    password = os.environ.get("E_KEY")
    email_to = os.environ.get("E_ID_TO")
    to = [email_to, receiver_email]
    message['From'] = my_email
    message['To'] = ", ".join(to)

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=my_email,
            password=password
        )
        return True
    except Exception as error:
        print(f"Error sending email to {to}: {str(error)}")
        return False


@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def contact():
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        if not verify_recaptcha(recaptcha_response):
            return render_template('contact.html', result="reCAPTCHA verification failed. Please try again.",
                                   success=False, site_key=site_key)

        name = sanitize_input(request.form.get('name', ''))
        phone = sanitize_input(request.form.get('phone', 'Not given'))
        email = sanitize_input(request.form.get('email', ''))
        subject = sanitize_input(request.form.get('subject', f'A new message from {name}'))
        message = sanitize_input(request.form.get('message', ''))

        if not name or not email or not message:
            return render_template('contact.html', result="Please fill all required fields", success=False)
        if not validate_email(email):
            return render_template('contact.html', result="Please enter a valid email address", success=False)

        body = f"Thank you for contacting me!\nNew message submitted.\n\nMessage:\n{message}\n\nName: {name}" \
               f"\nEmail: " \
               f"{email}\nPhone: {phone}"
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        asyncio.run(send_email_async(msg, email))

        return render_template('contact.html', result="Your message has been sent. We'll get back to you soon!",
                               success=True)
    return render_template('contact.html', result=False, site_key=site_key)


@app.route('/files/<int:num>')
def file(num):
    filename = f'assets/files/{num}.pdf'
    file_path = url_for('static', filename=filename)
    return redirect(file_path)


@app.route('/experience/ge/slides')
def slides():
    total = 23
    image_paths = []
    for x in range(1, total + 1):
        filename = f'assets/files/slides/Slide{x}.jpeg'
        image_path = url_for('static', filename=filename)
        image_paths.append(image_path)
    image_paths_with_index = [(index, path) for index, path in enumerate(image_paths)]
    return render_template('se.html', image_paths=image_paths_with_index, title="Thesis Seminar")


@app.route('/admin_slide/<int:num>/<d>/<t>')
@admin_only
@login_required
def admin_slide(num, d, t):
    decoded_t = unquote(t)
    total = num
    image_paths = []
    for x in range(1, total + 1):
        filename = f'assets/files/serve/{d}/Slide{x}.jpeg'
        image_path = url_for('static', filename=filename)
        image_paths.append(image_path)
    image_paths_with_index = [(index, path) for index, path in enumerate(image_paths)]
    return render_template('se.html', image_paths=image_paths_with_index, title=decoded_t)


@app.route('/l', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        if action == 'register':
            if users.find_one({'username': username}):
                flash('Username already exists.')
            else:
                user_id = str(users.count_documents({}) + 1)
                users.insert_one({'_id': user_id, 'username': username, 'password': hashed_password})
                flash('Registration successful.')
        elif action == 'login':
            user = users.find_one({'username': username})
            if user and check_password_hash(user['password'], password):
                user_obj = User(user['_id'], user['username'])
                login_user(user_obj)
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.')
    return render_template('login.html')


@app.route('/input')
def input_slides():
    return render_template('input.html')


@app.route('/save', methods=['POST'])
@admin_only
@login_required
def save_slides():
    name = request.form.get('name')
    title = request.form.get('title')
    urls = request.form.getlist('urls')

    document = {
        'name': name,
        'title': title,
        'urls': urls
    }
    collection_slides.insert_one(document)
    flash('Input done')

    return redirect('/input')


@app.route('/view/<name>')
@admin_only
@login_required
def view(name):
    document = collection_slides.find_one({'name': name})

    if document:
        urls = document.get('urls', [])
        title = document.get('title', 'Title Not found')
        urls_with_index = [(index, url) for index, url in enumerate(urls)]
    else:
        return

    return render_template('viewer.html', urls=urls_with_index, title=title)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user_status', methods=['GET'])
def user_status():
    if isinstance(current_user, AnonymousUserMixin):
        status = {'status': 0}
    elif int(current_user.id) != 1:
        status = {'status': 0}
    else:
        status = {'status': 1}
    return jsonify(status)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/experience')
def experience():
    return render_template('experience.html')


@app.route('/portfolio/sa')
def sa():
    return render_template('sa.html')


@app.route('/portfolio/ca')
def ca():
    return render_template('ca.html')


@app.route('/portfolio/ed')
def ed():
    return render_template('ed.html')


@app.route('/portfolio/ec')
def ec():
    return render_template('ec.html')


@app.route('/portfolio/er')
def er():
    return render_template('er.html')


@app.route('/portfolio/eo')
def eo():
    return render_template('eo.html')


@app.route('/experience/ee')
def ee():
    return render_template('ee.html')


@app.route('/experience/ge')
def ge():
    return render_template('ge.html')


@app.route('/experience/ae')
def ae():
    return render_template('ae.html')


if __name__ == '__main__':
    app.run(debug=False)
