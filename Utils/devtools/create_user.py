from uuid import uuid3, uuid1
from argon2 import PasswordHasher


def create_user(database, username, password, email, email_verified, admin):
    token = str(uuid3(uuid1(), str(uuid1())))
    hashed_password = PasswordHasher().hash(password)
    database.exec("""INSERT INTO cantina_administration.user(token, username, password, email, email_verified, admin) 
    VALUES (%s, %s, %s, %s, %s, %s)""", (token, username, hashed_password, email, email_verified, admin))
