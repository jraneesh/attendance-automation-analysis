import os, jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('./.env')

def encode_token(d,h, data, token_type):
    payload = {
            'exp' : datetime.utcnow() + timedelta(days=d, hours=h),
            'scope': token_type,
            'data' : data
    }
    return jwt.encode(
            payload, 
            os.environ['JWT_SECRET_KEY'],
            algorithm=os.environ['ALGORITHM']
    )

def decode_token(token,token_type):
    try:
        payload = jwt.decode(token,os.environ['JWT_SECRET_KEY'], os.environ['ALGORITHM'])
        if (datetime.utcnow()<=datetime.utcfromtimestamp(payload['exp'])):
            if (payload['scope'] == token_type):
                return payload['data']
            else: 
                return HTTPException(status_code=401, detail='Scope for the token is invalid')
        else:
            return HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')