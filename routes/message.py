import flask_mail

from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    request,
)
from routes import login_required
from models.message import Messages
from models.user import User
from setting import admin_mail

main = Blueprint('py_mail', __name__, static_folder='static')
mail = flask_mail.Mail()


@main.route("/add", methods=["POST"])
@login_required
def add(u):
    form = request.form.to_dict()
    form['receiver_id'] = int(form['receiver_id'])
    form['sender_id'] = u.id

    # 发邮件
    r = User.one(id=form['receiver_id'])
    m = flask_mail.Message(
        subject=form['title'],
        body=form['content'],
        sender=admin_mail,
        recipients=[r.email]
    )
    mail.send(m)

    Messages.new(form)
    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index(u):
    send = Messages.all(sender_id=u.id)
    received = Messages.all(receiver_id=u.id)

    t = render_template(
        './mail/index.html',
        user=u,
        send=send,
        received=received,
    )
    return t


@main.route('/view/<int:id>')
@login_required
def view(u, id):
    message = Messages.one(id=id)
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [message.receiver_id, message.sender_id]:
        return render_template('mail/detail.html', message=message)
    else:
        return redirect(url_for('py_mail.index'))
