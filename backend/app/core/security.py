import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

import bcrypt
if not hasattr(bcrypt, "__about__"):
    class _About:
        __version__ = getattr(bcrypt, "__version__", "5.0.0")
    bcrypt.__about__ = _About()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password with resilient fallback."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback to salted SHA-256 in environments where bcrypt native build might encounter edge issues
        salt = settings.SECRET_KEY[:16]
        expected = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return hmac.compare_digest(expected, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt with resilient fallback."""
    try:
        return pwd_context.hash(password)
    except Exception:
        salt = settings.SECRET_KEY[:16]
        return hashlib.sha256((salt + password).encode()).hexdigest()

def create_access_token(subject: Union[str, Any], role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate encoded JWT access token with role claim."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
