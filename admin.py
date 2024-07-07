from flask import abort, flash, redirect, url_for, Markup
from flask_login import current_user, AnonymousUserMixin
from functools import wraps


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, AnonymousUserMixin):
            flash(Markup(
                "You don't have the permission to access the requested resource. Please request through "
                "<a class='not-tag' href='{}'>form.</a>".format(url_for('main.contact'))), "error")
            return redirect(url_for("main.error", allowed=0))

        if int(current_user.id) != 1:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function
