from flask import current_app, url_for, redirect
from models.transactions import find_one
import requests
import aiosmtplib
import re
import html


def sanitize_input(user_input):
    return html.escape(user_input.strip())


def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) is not None


async def verify_recaptcha(response):
    secret_key = current_app.config['RECAPTCHA_SECRET_KEY']
    payload = {'secret': secret_key, 'response': response}
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result.get('success', False)


async def send_email_async(message, receiver_email):
    email_username = current_app.config['EMAIL_USER']
    email_to = current_app.config['EMAIL_RECEIVER']
    to = [email_to, receiver_email]
    message['From'] = email_username
    message['To'] = ", ".join(to)

    try:
        await aiosmtplib.send(
            message,
            hostname=current_app.config['EMAIL_HOST'],
            port=current_app.config['EMAIL_PORT'],
            start_tls=True,
            username=email_username,
            password=current_app.config['EMAIL_PASSWORD']
        )
        return True
    except Exception as error:
        print(f"Error sending email to {to}: {str(error)}")
        return False


async def serve_file_by_num(num):
    filename = f'assets/files/{num}.pdf'
    return redirect(url_for('static', filename=filename))


async def serve_admin_slides(num, d):
    total = num
    image_paths = []
    for x in range(1, total + 1):
        filename = f'assets/files/serve/{d}/Slide{x}.jpeg'
        image_path = url_for('static', filename=filename)
        image_paths.append(image_path)
    return [(index, path) for index, path in enumerate(image_paths)]


async def retrieve_db_slides(name):
    document = find_one("slidesviewer", "slides", {'name': name})
    urls = document.get('urls', [])
    title = document.get('title', 'Title Not found')
    urls_with_index = [(index, url) for index, url in enumerate(urls)]
    return title, urls_with_index


async def serve_slides_thesis():
    total = 23
    image_paths = []
    for x in range(1, total + 1):
        filename = f'assets/files/slides/Slide{x}.jpeg'
        image_path = url_for('static', filename=filename)
        image_paths.append(image_path)
    return [(index, path) for index, path in enumerate(image_paths)]
