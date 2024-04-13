import binascii
import json
from typing import Any, Dict
import base64
import random

SESSION_KEY_BYTE_LENGTH = 16


class HTTPSession:
    def __init__(self, key: str, expire: Any) -> None:
        self.key = key
        self.expire = expire

    def encrypt(self):
        return base64.b64encode(('{"key": "' + self.key + '"}').encode()).decode()

    @classmethod
    def decrypt(cls, session_cookie: str) -> 'HTTPSession':
        try:
            session = json.loads(base64.b64decode(session_cookie))
            return cls.from_json(session)
        except (binascii.Error, UnicodeDecodeError, json.decoder.JSONDecodeError):
            return False

    @classmethod
    def from_json(cls, session_json: dict) -> 'HTTPSession':
        key = session_json.get('key')
        expire = session_json.get('expire')
        return cls(key, expire)

    @staticmethod
    def _generate_session_key():
        return base64.b64encode(random.randbytes(SESSION_KEY_BYTE_LENGTH)).decode()


if __name__ == '__main__':
    key = HTTPSession._generate_session_key()
    print(key)
    encrypted = HTTPSession(key, None).encrypt()
    print(encrypted)
    print(HTTPSession.decrypt(encrypted).key)
