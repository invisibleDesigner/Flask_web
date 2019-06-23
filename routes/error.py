from flask import (
    render_template,
    Blueprint,
)

main = Blueprint('py_error', __name__, static_folder='static')


@main.app_errorhandler(404)
def not_found(e):
    return render_template('error/error.html')


@main.app_errorhandler(401)
def no_login(e):
    return render_template('error/401.html')


@main.app_errorhandler(403)
def no_access(e):
    return render_template('error/403.html')


