import time
from typing import Dict, Union
import jwt
from decouple import config
import logging

# Load environment variables
JWT_SECRET_KEY = config('SECRET', default='secret')
DEBUG = config('DEBUG', default=True, cast=bool)

# Algorithm used to sign the JWT token
JWT_ALGORITHM = 'HS256'

# Logging configuration
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

def signJWT(username: str, expiration: int = 3600) -> str:
    """
    Signs a JWT token with the given username and expiration time.
    :param username: The username to include in the token.
    :param expiration: The expiration time in seconds. Defaults to 3600 seconds (1 hour).
    :return: Encoded JWT token as a string.
    """
    payload = {
        "username": username,
        "exp": time.time() + expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    logger.debug(f"Generated token for user {username}")
    return token

def decodeJWT(token: str) -> Union[Dict, None]:
    """
    Decodes a JWT token and returns the payload.
    :param token: The JWT token to decode.
    :return: The decoded payload if the token is valid, otherwise an error message.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        logger.debug(f"Decoded token payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return {"error": "Invalid token"}
    except Exception as e:
        logger.error(f"Error occurred while decoding JWT: {e}")
        return None

def extract_jwt_username(token: str) -> str:
    """
    Extracts the username from a JWT token.
    :param token: The JWT token.
    :return: The username from the token payload.
    """
    payload = decodeJWT(token)
    if "username" in payload:
        return payload["username"]
    return ""
