import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from typing import Dict, Any
import os


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


def create_access_token(payload: Dict[str, Any]) -> str:
    """
    Create a JWT access token with 1 day expiry.

    Args:
        payload: Dictionary containing the token claims

    Returns:
        str: Generated JWT token

    Raises:
        ValueError: If payload is invalid
        Exception: If token generation fails
    """
    if not payload or not isinstance(payload, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    try:
        expire = datetime.utcnow() + timedelta(days=1)
        payload.update({"exp": expire, "type": "access"})

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        raise Exception(f"Failed to create access token: {str(e)}")


def create_session_token(payload: Dict[str, Any]) -> str:
    """
    Create a JWT session token with 10 days expiry.

    Args:
        payload: Dictionary containing the token claims

    Returns:
        str: Generated JWT token

    Raises:
        ValueError: If payload is invalid
        Exception: If token generation fails
    """
    if not payload or not isinstance(payload, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    try:
        expire = datetime.utcnow() + timedelta(days=10)
        payload.update({"exp": expire, "type": "session"})

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        raise Exception(f"Failed to create session token: {str(e)}")


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except InvalidTokenError:
        raise Exception("Invalid token")
