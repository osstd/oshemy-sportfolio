from flask import Flask, render_template, request
from email.mime.text import MIMEText
import smtplib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')


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
            return "Email sent successfully!"
    except smtplib.SMTPException as e:
        return f"Error sending email: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


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
        body = f"Thank you for contacting me!\nNew message submitted.\n\nMessage:\n{message}\n\nName: {name}\nEmail: {email}\nPhone: {phone}"
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        result = send_email(msg, receiver_email)
        # flash(result)
        return render_template('contact.html', result=result)
    return render_template('contact.html', result=False)


if __name__ == '__main__':
    app.run(debug=True)
