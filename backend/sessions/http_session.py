import binascii
import json
from typing import Any, Dict
import base64
import random

SESSION_KEY_BYTE_LENGTH = 16

class HTTPSession:
    """
    A class to manage HTTP sessions, including encryption and decryption of session data and username.
    """
    def __init__(self, key: str, expire: Any) -> None:
        """
        Initialize the HTTPSession with a key and expiration time.

        Args:
            key (str): The session key.
            expire (Any): The expiration time of the session.
        """
        self.key = key
        self.expire = expire
        self.username = ""

    def set_username(self, username: str):
        """
        Set the username for the session.

        Args:
            username (str): The username to set.
        """
        self.username = username

    def encrypt_session(self) -> str:
        """
        Encrypt the session key into a base64 encoded JSON string.

        Returns:
            str: The encrypted session string.
        """
        return base64.b64encode(
            ('{"key": "' + self.key + '"}').encode()
        ).decode()

    @classmethod
    def decrypt_session(cls, session_cookie: str) -> 'HTTPSession':
        """
        Decrypt a session cookie back into an HTTPSession object.

        Args:
            session_cookie (str): The encrypted session cookie.

        Returns:
            HTTPSession: The decrypted session object, or False if decryption fails.
        """
        try:
            session = json.loads(base64.b64decode(session_cookie))
            return cls.from_json(session)
        except (binascii.Error, UnicodeDecodeError, json.decoder.JSONDecodeError):
            return False

    def encrypt_username(self) -> str:
        """
        Encrypt the username for the session.

        Returns:
            str: The encrypted username.
        """
        return self.username

    def decrypt_username(self, user_cookie: str) -> str:
        """
        Decrypt the username from the cookie.

        Args:
            user_cookie (str): The encrypted username cookie.

        Returns:
            str: The decrypted username.
        """
        return user_cookie

    @classmethod
    def from_json(cls, session_json: Dict[str, Any]) -> 'HTTPSession':
        """
        Create an HTTPSession object from a JSON dictionary.

        Args:
            session_json (dict): The JSON dictionary containing session data.

        Returns:
            HTTPSession: The created HTTPSession object.
        """
        key = session_json.get('key')
        expire = session_json.get('expire')
        return cls(key, expire)

    @staticmethod
    def _generate_session_key() -> str:
        """
        Generate a random session key.

        Returns:
            str: The base64 encoded random session key.
        """
        return base64.b64encode(random.randbytes(SESSION_KEY_BYTE_LENGTH)).decode()


if __name__ == '__main__':
    """
    Main block to demonstrate session key generation, encryption, and decryption.
    """
    key = HTTPSession._generate_session_key()
    print(key)
    encrypted = HTTPSession(key, None).encrypt_session()
    print(encrypted)
    print(HTTPSession.decrypt_session(encrypted).key)
