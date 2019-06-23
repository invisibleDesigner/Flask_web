import secret
import setting

from utils import log, format_time, last_active_time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db
from models.user import User
from models.topic import Topic
from models.reply import Reply

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.message import main as mail_routes, mail
from routes.error import main as error_routes


def configured_app():
    """配置app"""
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    app.secret_key = setting.secret_key
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+mysqlconnector://root:{}@localhost/PythonForum?charset=utf8mb4'.format(secret.database_password)
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = setting.admin_mail
    app.config['MAIL_PASSWORD'] = secret.mail_password
    mail.init_app(app)

    """载入蓝图"""
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(error_routes)

    """载入过滤器"""
    app.template_filter()(format_time)
    app.template_filter()(last_active_time)

    """载入后台管理系统"""
    admin = Admin(app, name='PythonForum', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))
    return app


def main():
    app = configured_app()
    # 主要用来启动development模式
    config = dict(
        host='localhost',
        port=5000,
    )
    app.run(**config)


if __name__ == '__main__':
    main()
