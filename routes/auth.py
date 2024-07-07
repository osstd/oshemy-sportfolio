from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import limiter
from models.models import User
from models.transactions import get_collection, find_one, insert_one, DatabaseError
from utils import sanitize_input

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/user_status', methods=['GET'])
def user_status():
    if isinstance(current_user, AnonymousUserMixin):
        status = {'status': 0}
    elif int(current_user.id) != 1:
        status = {'status': 0}
    else:
        status = {'status': 1}
    return jsonify(status)


@auth_bp.route('/l', methods=['GET', 'POST'])
@limiter.limit("15 per hour")
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = sanitize_input(request.form.get('username'))
        password = request.form.get('password')

        try:
            if action == 'register':
                if find_one("portfoliopage", "portfolio_users", {'username': username}):
                    flash('Username already exists, please login instead', 'error')
                    return redirect(url_for('auth.auth'))

                user_id = str(get_collection("portfoliopage", "portfolio_users").count_documents({}) + 1)
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                insert_one("portfoliopage", "portfolio_users",
                           {'_id': user_id, 'username': username, 'password': hashed_password})
                flash('Registration successful, please login now', 'success')
                return redirect(url_for('auth.auth'))

            elif action == 'login':
                user = find_one("portfoliopage", "portfolio_users", {'username': username})

                if not user or not check_password_hash(user['password'], password):
                    if not user:
                        flash('Invalid username, please try again', 'error')
                    if user and not check_password_hash(user['password'], password):
                        flash('Invalid password, please try again', 'error')
                    return redirect(url_for('auth.auth'))

                login_user(User(user['_id'], user['username']))
                return redirect(url_for('main.home'))

        except DatabaseError as e:
            flash(f"An error occurred:{e}", "error")
            return redirect(url_for("auth.auth"))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
