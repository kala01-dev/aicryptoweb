import bcrypt

def check_password(password: str, hashed: str) -> bool:
    """Verifikasi password terhadap hash bcrypt."""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        return False
