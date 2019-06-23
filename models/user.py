import hashlib
import setting
from sqlalchemy import Column, String, Boolean
from models import SQLMixin, db


def sha256(ascii_str):
    return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()


class User(SQLMixin, db.Model):

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    avatar = Column(String(256), nullable=False)
    signature = Column(String(256), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    email = Column(String(50), nullable=False, default=setting.test_mail)

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        username = form['username']
        password = form['password']
        if len(password) >= 3 and len(username) >= 3 and User.one(username=username) is None:
            u = User.new(form)
            u.password = u.salted_password(password)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(username=form['username'])
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None
