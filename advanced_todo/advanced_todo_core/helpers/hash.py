from datetime import datetime, timedelta
from jose import jwt, JWTError
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ENCRYPTION_EXPIRE_MINUTES = 10

class Hash():
    
    def bcrypt(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ENCRYPTION_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify(hased_text, text):
        try:
            payload = jwt.decode(hased_text, SECRET_KEY, algorithms=[ALGORITHM])
            key = payload.get("key")
            if text == key:
                return True
            else:
                return False
        except JWTError:
            return False


