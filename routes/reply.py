import time

from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.reply import Reply

from utils import log


main = Blueprint('py_reply', __name__, static_folder='static')


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Reply.add(form, user_id=u.id)
    # log('======== reply add()  m =========\n{}'.format(m))
    return redirect(url_for('py_topic.detail', id=m.topic_id))

