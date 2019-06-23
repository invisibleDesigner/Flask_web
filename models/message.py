from sqlalchemy import Column, Unicode, UnicodeText, Integer
from models import SQLMixin, db
from models.user import User


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @classmethod
    def get_sender_name(cls):
        u = User.one(id=cls.sender_id)
        return u.name

    @classmethod
    def get_receiver_name(cls):
        u = User.one(id=cls.receiver_id)
        return u.name
