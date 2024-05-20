# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
import jwt
from decouple import config

JWT_SECRET_KEY = config('SECRET', default='secret')
DEBUG = config('DEBUG', default=True, cast=bool)
# algorithm used to sign the token
JWT_ALGORITHM = 'HS256'

print(f"Secret Key: {JWT_SECRET_KEY}")
print(f"Debug Mode: {DEBUG}")
print(f"Secret Algorithm: {JWT_ALGORITHM}")





# create function to return generated tokens (JWTs)
def create_access_token(token: str):
    return {
        "access token": token
        # what happens is that these JSN tokens are encoded into str
    }
    

# Function used for signing the JWT string
def signJWT(userID: str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    # we pass the token as input in the token response
    return create_access_token(token)

# Function that 
def decodeJWT(token: str):
    try:

        decode_token = jwt.decode(token, JWT_SECRET_KEY,algorithms=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}