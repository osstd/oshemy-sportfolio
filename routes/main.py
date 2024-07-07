from flask import Blueprint, render_template, request, current_app
from extensions import limiter
from utils import validate_email, sanitize_input, verify_recaptcha, send_email_async
from admin import admin_only
from email.mime.text import MIMEText
import asyncio

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('index.html')


@main_bp.route('/services')
def services():
    return render_template('services.html')


@main_bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@main_bp.route('/experience')
def experience():
    return render_template('experience.html')


@main_bp.route('/error')
def error():
    allowed = request.args.get('allowed', default=None, type=int)
    admin_cond = True

    if allowed is not None and allowed == 0:
        admin_cond = False

    return render_template('error.html', admin=admin_cond)


@main_bp.route('/admin')
@admin_only
def admin():
    return render_template('admin.html')


@main_bp.route('/portfolio/sa')
def sa():
    return render_template('sa.html')


@main_bp.route('/portfolio/ca')
def ca():
    return render_template('ca.html')


@main_bp.route('/portfolio/ed')
def ed():
    return render_template('ed.html')


@main_bp.route('/portfolio/ec')
def ec():
    return render_template('ec.html')


@main_bp.route('/portfolio/er')
def er():
    return render_template('er.html')


@main_bp.route('/portfolio/eo')
def eo():
    return render_template('eo.html')


@main_bp.route('/experience/ee')
def ee():
    return render_template('ee.html')


@main_bp.route('/experience/ge')
def ge():
    return render_template('ge.html')


@main_bp.route('/experience/ae')
def ae():
    return render_template('ae.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def contact():
    if request.method == 'POST':

        recaptcha_response = request.form['g-recaptcha-response']
        if not asyncio.run(verify_recaptcha(recaptcha_response)):
            return render_template('contact.html', result="reCAPTCHA verification failed. Please try again.",
                                   success=False, site_key=current_app.config['RECAPTCHA_SITE_KEY'])

        name = sanitize_input(request.form.get('name', ''))
        phone = sanitize_input(request.form.get('phone', 'Not given'))
        email = request.form.get('email', '').lower().strip()
        subject = sanitize_input(request.form.get('subject', f'A new message from {name}'))
        message = sanitize_input(request.form.get('message', ''))

        if not all([name, email, message]):
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
    return render_template('contact.html', result=False, site_key=current_app.config['RECAPTCHA_SITE_KEY'])
