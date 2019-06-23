try:
    import sys
    sys.path.append('../')
except ModuleNotFoundError:
    print(ModuleNotFoundError)

import secret

from app import configured_app

from models import db
from models.user import User
from models.topic import Topic
from models.board import Board
from models.message import Messages

from sqlalchemy import create_engine


def reset_database():
    url = 'mysql+mysqlconnector://root:{}@localhost:3306/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS PythonForum')
        c.execute('CREATE DATABASE PythonForum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE PythonForum')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    # 造两条用户数据
    form = dict(
        username='123qwe',
        password='123qwe',
        avatar='/static/img/1.jpg',
        name='杨畅',
        signature='这家伙很懒，什么个性签名都没有留下。',
        is_admin=True,
        email='15200993016@163.com'
    )
    u = User.register(form)

    form = dict(
        username='qwe123',
        password='123qwe',
        avatar='/static/img/1.jpg',
        name='畅畅',
        signature='这家伙很懒，什么个性签名都没有留下。',
        email='15200993016@163.com',
    )
    u = User.register(form)

    # 造三个基础board
    form = dict(
        title='爬虫',
    )
    Board.new(form)
    form = dict(
        title='数据分析',
    )
    Board.new(form)
    form = dict(
        title='web后端',
    )
    Board.new(form)

    # 造三条话题数据
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown 爬虫',
        content=content,
        views=0,
        board_id=1,
    )
    Topic.add(form, u.id)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown 数据分析',
        content=content,
        views=0,
        board_id=2,
    )
    Topic.add(form, u.id)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown web后端',
        content=content,
        views=0,
        board_id=3,
    )
    Topic.add(form, u.id)

    # 为一个用户，创建多个话题
    for i in range(100):
        with open('markdown_demo.md', encoding='utf8') as f:
            content = f.read()
        form = dict(
            title='topic_demo_{}'.format(i),
            content=content,
            views=0,
            board_id=3,
        )
        Topic.add(form, 1)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
