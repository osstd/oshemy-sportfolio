from flask import Flask, abort, render_template, request, redirect, url_for, render_template_string, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from email.mime.text import MIMEText
from urllib.parse import unquote
import smtplib
import os


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, AnonymousUserMixin):
            return "You don't have the permission to access the requested resource. Please contact for the slides."
        if int(current_user.id) != 1:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

# Send a ping to confirm a successful connection to the mongo server no creation
client = mongo.cx

try:
    client.admin.command('ping')
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    flash(f"Failed to connect to MongoDB: {e}")

db = client.portfoliopage
users = db.portfolio_users

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


def send_email(message, receiver_email):
    my_email = os.environ.get("E_ID")
    password = os.environ.get("E_KEY")
    email_to = os.environ.get("E_ID_TO")
    to = [email_to, receiver_email]
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=to,
                                msg=message.as_string())
            connection.close()
            return ["Email sent successfully!", 1]
    except smtplib.SMTPException as e:
        return [f"Error sending email: {e}", 0]
    except Exception as e:
        return [f"Unexpected error: {e}", 0]


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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        if request.form['phone']:
            phone = request.form['phone']
        else:
            phone = 'Not given'
        email = request.form['email']
        receiver_email = email
        if request.form['subject']:
            subject = request.form['subject']
        else:
            subject = f'A new message from {name}'
        message = request.form['message']

        subject = subject
        body = f"Thank you for contacting me!\nNew message submitted.\n\nMessage:\n{message}\n\nName: {name}\nEmail: " \
               f"{email}\nPhone: {phone}"
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        result = send_email(msg, receiver_email)
        if result[1] == 1:
            return render_template('contact.html', result=result[0], success=True)
        else:
            return render_template('contact.html', result=result[0], success=False)
    return render_template('contact.html', result=False)


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
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        if action == 'register':
            print("register route")
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/user_status', methods=['GET'])
def user_status():
    if isinstance(current_user, AnonymousUserMixin):
        status = {'status': 0}
    elif int(current_user.id) != 1:
        status = {'status': 0}
    else:
        status = {'status': 1}
    return jsonify(status)


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
    app.run(debug=True)
