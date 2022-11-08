import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from datetime import datetime, timedelta
from config.config import config

SECRET_KEY = config['conf']['web']['SECRET_KEY']


def judge_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        # print(payload)
        return payload
    except ExpiredSignatureError:
        # print('token过期了')
        return None
    except PyJWTError:
        # print('token验证失败')
        return None


def create_token(username, user_id):
    expires = datetime.utcnow() + timedelta(hours=1)
    to_encode = {'exp': expires, 'user': username, 'id': user_id}
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encode_jwt
