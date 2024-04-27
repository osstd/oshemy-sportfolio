from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('se.html', image_paths=image_paths_with_index)


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
