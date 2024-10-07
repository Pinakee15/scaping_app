from fastapi import Header, HTTPException
from typing import Optional

class AuthHandler:
    def __init__(self, token: str):
        self.token = token

    def authenticate(self, token: Optional[str] = Header(None)):
        if token != self.token:
            raise HTTPException(status_code=401, detail="Unauthorized")

