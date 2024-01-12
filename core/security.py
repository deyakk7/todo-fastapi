from passlib import context

pwd_context = context.CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(current_password, hashed_password):
    return pwd_context.verify(current_password, hashed_password)
