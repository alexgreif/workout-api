from pwdlib import PasswordHash

pwd_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return pwd_hasher.verify(password, password_hash)
    except Exception:
        return False