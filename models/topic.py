from sqlalchemy import (
    Integer,
    Column,
    UnicodeText,
    Unicode,
    ForeignKey,
)
from sqlalchemy.orm import relationship


from models import SQLMixin, db
from models.user import User
from models.reply import Reply
from models.board import Board


class Topic(SQLMixin, db.Model):

    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    views = Column(Integer, nullable=False)
    board_id = Column(Integer, ForeignKey('board.id'), nullable=False)
    board = relationship(Board, backref="topic_of_board")

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = cls.new(form)
        return m

    @classmethod
    def get(cls, _id):
        m = cls.one(id=_id)
        m.views += 1
        m.save()
        return m

    def owner(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def reply_of_user(self, user_id):
        reply = Reply.one(topic_id=self.id, user_id=user_id)
        return reply
