import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    flash,
)

from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from routes import login_required

from models.user import User
from models.topic import Topic
from models.reply import Reply
from utils import log


import redis
import json

cache = redis.StrictRedis(host='localhost', port=6379, db=0, password='')

"""
    访问首页
    注册
    登录
    用户登录后, 会写入 session, 并且定向到 topic index页面
"""
main = Blueprint('index', __name__, static_folder='static')


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form: ImmutableMultiDict = request.form
    form = form.to_dict()
    form['avatar'] = '/static/img/1.jpg'
    form['signature'] = '这家伙很懒，什么个性签名都没有留下。'
    u = User.register(form)
    log("注册用户为：{}".format(u))
    if u is None:
        flash("注册失败！", 'register')
        return redirect(url_for('.index', register='false'))
    else:
        flash("注册成功！")
        return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        flash("登录失败！", 'login')
        return redirect(url_for('.index', login='false'))
    else:
        log("登录用户为：{}".format(u))
        session['user_id'] = u.id
        session.permanent = True
        # log("当前session列表为：{}".format(session))
        return redirect(url_for('py_topic.index'))


@main.route("/sign_out", methods=['GET'])
def sign_out():
    session.clear()
    return redirect(url_for('.index'))


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        k = 'topics_{}'.format(id)
        if cache.exists(k):
            v = cache.get(k)
            topics = json.loads(v)
            print("正在使用缓存")
        else:
            topics: list = Topic.all(user_id=u.id)
            topics.sort(key=lambda i: i.created_time, reverse=True)

            replys: list = Reply.all(user_id=u.id)
            print('<user_detail replys {}'.format(replys))
            re_topics = []
            for reply in replys:
                topic = Topic.one(id=reply.topic_id)
                if topic not in re_topics:
                    re_topics.append(topic)
            print('<user_detail re_topics {}'.format(re_topics))
            v = json.dumps([t.json() for t in topics])
            cache.set(k, v)

        return render_template('user/profile.html', user=u, topics=topics, re_topics=[])


@main.route('/setting')
@login_required
def setting(u):
    return render_template('./user/setting.html', user=u)


@main.route('/setting/update_information', methods=['POST'])
@login_required
def setting_update_information(u):
    form = request.form
    u.username = form['name']
    u.signature = form['signature']
    u.save()
    return redirect(url_for('.setting'))


@main.route('/setting/update_password', methods=['POST'])
@login_required
def setting_update_password(u):
    form = request.form
    old_pass = form['old_pass']
    old_pass_s = User.salted_password(old_pass)
    new_pass = form['new_pass']
    new_pass_s = User.salted_password(new_pass)
    if old_pass_s == u.password:
        u.password = new_pass_s
        u.save()
    return redirect(url_for('.setting'))


@main.route('/setting/add_avatar', methods=['POST'])
@login_required
def add_avatar(u):
    print(request.files)
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('./static/img', filename)
    file.save(path)
    User.update(u.id, avatar='./static/img/{}'.format(filename))
    return redirect(url_for('.setting'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('/static/img', filename)
