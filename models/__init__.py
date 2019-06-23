import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()


class SQLMixin(object):

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=int(time.time()))
    updated_time = Column(Integer, default=int(time.time()))

    @classmethod
    def new(cls, form):
        m = cls()
        # 时间默认是写死的，所以要传递一个活的
        form['created_time'] = time.time()
        form['updated_time'] = time.time()
        for name, value in form.items():
            setattr(m, name, value)
        m.save()
        return m

    @classmethod
    def update(cls, _id, **kwargs):
        m = cls.query.filter_by(id=_id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.save()

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d
