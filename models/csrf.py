import redis
import uuid


class Csrf:

    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

    @staticmethod
    def generate_csrf():
        Csrf.r.set('csrf_token', str(uuid.uuid4()))

    @staticmethod
    def get_csrf():
        return Csrf.r.get('csrf_token')
