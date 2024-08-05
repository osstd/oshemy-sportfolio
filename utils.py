from flask import current_app, url_for, redirect
from models.transactions import find_one, insert_one, DatabaseError
from datetime import datetime
from aiohttp import ClientTimeout
from aiohttp.client_exceptions import ClientError
import aiosmtplib
import aiohttp
import asyncio
import requests
import re
import html
import pytz

from logging_config import setup_logging

logger = setup_logging()


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


async def get_ip_address(request):
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logger.info(f"Your IP address is: {visitor_ip}")

    tz = pytz.timezone('America/New_York')
    current_time_tz = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)
    current_time = current_time_tz.strftime('%Y-%m-%d %H:%M:%S')

    try:
        timeout = ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'https://ipapi.co/{visitor_ip}/json/') as response:
                if response.status == 200:
                    geolocation_data = await response.json()
                    city = geolocation_data.get('city', 'Unknown')
                    country = geolocation_data.get('country_name', 'Unknown')
                else:
                    logger.warning(f"API returned status code {response.status}")
                    city = country = 'Unknown'
    except asyncio.TimeoutError:
        logger.error("Request to ipapi.co timed out")
        city = country = 'Unknown'
    except ClientError as e:
        logger.error(f"Error occurred while fetching geolocation data: {str(e)}")
        city = country = 'Unknown'
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        city = country = 'Unknown'

    document = {
        'ip_address': visitor_ip,
        'city': city,
        'country': country,
        'datetime': current_time
    }

    try:
        insert_one("ip_visitors", "sportfolio", document)
        logger.info(f"{'Known' if city != 'Unknown' else 'Unknown'} insert successful")
    except DatabaseError as e:
        logger.error(f"Error inserting document into database: {str(e)}")

    return visitor_ip

