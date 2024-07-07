from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from models.transactions import get_collection, delete_one, DatabaseError
from admin import admin_only

users_bp = Blueprint('users', __name__)


@users_bp.route('/view-users')
@admin_only
@login_required
def view_users():
    try:
        users = get_collection("portfoliopage", "portfolio_users").find({}, {"_id": 1, "username": 1})
        return render_template('view-directory.html', users=users, title="Users")

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@users_bp.route('/delete-user/<user_id>', methods=['GET', 'POST'])
@admin_only
@login_required
def delete_user(user_id):
    try:
        delete_one("portfoliopage", "portfolio_users", {"_id": user_id})
        flash("User successfully deleted", "success")
    except DatabaseError as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for("users.view_users"))
