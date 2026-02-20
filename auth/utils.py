# auth/utils.py
import re
import bcrypt

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def valid_username(u: str) -> bool:
    return bool(USERNAME_RE.match(u or ""))

def valid_email(e: str) -> bool:
    return (not e) or bool(EMAIL_RE.match(e))
