import datetime
import hmac
import sqlite3
import bcrypt
from protocol import Protocol


def _hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


GARBAGE_PASSWORD = _hash_password("garbage").encode()


class Database:
    __instance = None

    def __init__(self, file_location) -> None:
        self.conn = sqlite3.connect(file_location)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def sign_up(self, username: str, country: str, email: str, password: str):
        # Check if username or email is already in the database
        self.cursor.execute('''
            SELECT username FROM users WHERE email==(?) OR username==(?)
        ''', (email, username))
        user = self.cursor.fetchall()
        if user:
            print(user)
            return Protocol.Error.user_already_exists

        # Success
        self._register_user(username, country, email, password)
        return Protocol.success

    def _register_user(self, username: str, country: str, email: str, password: str):
        print(password)
        hashed_password = _hash_password(password)
        print(hashed_password)
        self.cursor.execute('''
            INSERT INTO users (username, country, email, password)
            VALUES (?, ?, ?, ?)
        ''', (username, country, email, hashed_password))
        self.conn.commit()

    def log_in(self, email: str, password: str):
        flag = True  # prevent timing based attack
        print(password)
        self.cursor.execute('''
            SELECT password FROM users WHERE email==(?)
        ''', (email,))

        db_passwords = self.cursor.fetchall()
        if not db_passwords:
            flag = False
            db_password = GARBAGE_PASSWORD
        else:
            db_password = db_passwords[0][0].encode()

        flag = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=db_password
        )
        return Protocol.success if flag else flag

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                country TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_user_info_by_email(self, email: str) -> str:
        """fetch username form the database with an email.

        Args:
            email (str): email

        Returns:
            str: username"""
        
        self.cursor.execute('''
            SELECT username FROM users WHERE email==(?)
        ''', (email,))
        
        username = self.cursor.fetchone()
        if not username:
            return None
        else:
            return username[0]

    def clear(self):
        self.cursor.execute('''
            DELETE FROM users
        ''')

    @classmethod
    def get_instance(cls, file_location):
        if cls.__instance is not None:
            return cls.__instance
        cls.__instance = cls(file_location)
        return cls.__instance

# database = Database.get_instance('users.db')
# database.clear()


if __name__ == '__main__':
    # start = datetime.datetime.now()
    # for i in range(1_000):
    #     _hash_password("john_pit@")
    # print(datetime.datetime.now() - start)

    database = Database.get_instance('users.db')
    # database.clear()

    username = "donde"
    email = "pablo_my_love@gmail.com"
    birthday = "01/01/1999"
    password = "1999donde@"
    # database.register_user(username, email, birthday, password)

    print(database.log_in("pablo_my_love@gmail.com", "1999donde@"))

    database.close()

# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

# class Base(DeclarativeBase):
#     pass

# class User(Base):
#     __tablename__ = "user_account"

#     id: Mapped[int]
#     username = Mapped[str]

#     def __repr__(self) -> str:
#         return f"User(id={self.id}, username={self.username})"
