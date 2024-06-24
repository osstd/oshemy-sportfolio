# Engineering Web App Showcase

I built this web app as a tool to showcase my structural engineering technical skills and projects.
This is a Flask application that serves as a portfolio site and a slides' viewer. The app allows users to contact the site owner, view slides, and access different sections of the portfolio. Additionally, there are admin-only features for managing slide content.

## Features

- View experience projects and demonstrations
- Presenter slide show and navigating different slides
- Admin user authentication to access parts of the app
  - Show certain components when admin is using the app in presenting mode vs when users are browsing it
- Contact email validation and handling
- User authentication (login and registration)
- Admin-only access for managing slide content
- Contact form with email notifications
- Portfolio sections
- Slides viewer

## Technology Used

- **Programming Language:** Python
- **Frameworks:** Flask, Bootstrap5
- **Frontend:** HTML, CSS, JavaScript
- **Packages:** FlaskForm, wtforms, twilio

## Requirements

- Python 3.7+
- Flask
- Flask-Login
- Flask-PyMongo
- Werkzeug
- smtplib (for email notifications)
- MongoDB

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/osstd/oshemy-sportfolio.git
    cd portfolio_app
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables. Create a `.env` file in the project root directory and add the following:

    ```env
    F_KEY=your_secret_key
    MONGO_URI=your_mongo_uri
    E_ID=your_email_id
    E_KEY=your_email_password
    E_ID_TO=receiver_email_id
    ```

    Replace `your_secret_key` with a secret key for your Flask application, `your_mongo_uri` with your MongoDB connection URI, and email-related environment variables with appropriate values.

5. Run the application:

    ```bash
    flask run
    ```

## Usage

### Routes

- `/` : Home page
- `/login` : User login page
- `/logout` : User logout
- `/contact` : Contact form page
- `/files/<int:num>` : Redirect to a file
- `/experience/ge/slides` : View slides for a specific experience
- `/admin_slide/<int:num>/<d>/<t>` : Admin-only route to view slides with decoded title
- `/l` : Authentication page (login and registration)
- `/input` : Admin-only input form for slides
- `/save` : Admin-only route to save slides
- `/view/<name>` : Admin-only route to view slides by name
- `/user_status` : Get the current user status (admin or not)
- `/services` : Services page
- `/portfolio` : Portfolio main page
- `/portfolio/sa` : Portfolio subpage Structural Analysis
- `/portfolio/ca` : Portfolio subpage Component Analysis
- `/portfolio/ed` : Portfolio subpage Engineering Drawing
- `/portfolio/ec` : Portfolio subpage Engineering Calculations
- `/portfolio/er` : Portfolio subpage Engineering Reports
- `/portfolio/eo` : Portfolio subpage Engineering Observations
- `/experience` : Experience main page
- `/experience/ee` : Experience subpage Professional Experience
- `/experience/ge` : Experience subpage Graduate Experience 
- `/experience/ae` : Experience subpage Awards

### Admin-Only Features

The application includes a decorator `@admin_only` that restricts access to certain routes to the admin user (user with ID 1).

### Email Notifications

The contact form sends email notifications using the `smtplib` module. Ensure your email credentials are set up in the environment variables.

## Database Models

- `User` : Represents a user in the application (stored in MongoDB)
- `collection_slides` : Stores slide documents with names, titles, and URLs

