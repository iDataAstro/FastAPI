from passlib.context import CryptContext


# Creating password context
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pass_context.hash(password)


def verify_password(plain_password: str, db_hash_password: str):
    return pass_context.verify(plain_password, db_hash_password)
