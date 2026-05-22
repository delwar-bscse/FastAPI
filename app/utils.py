import logging
from pwdlib import PasswordHash

# Setup a basic logger to track hashing errors safely
logger = logging.getLogger(__name__)

password_hasher = PasswordHash.recommended()

"""Hashes a plain text password. Raises ValueError if hashing fails."""
def hash_password(password: str) -> str:
    try:
        return password_hasher.hash(password)
    except ValueError as e:
        logger.error(f"Password hashing failed: {e}")
        # Reraise the error or raise a custom HTTP exception instead of returning False
        raise ValueError("Could not process password security hashing.")

"""Verifies a plain text password against its hash."""
def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(password, hashed_password)
    except Exception as e:
        # Catch all issues (like malformed hash strings) and log them
        logger.error(f"Password verification error encountered: {e}")
        return False