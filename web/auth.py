from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

admins = ["admin"]
users = ["user", "admin"]

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in admins:
        return {"username": credentials.username, "role": "admin"}
    elif credentials.username in users:
        return {"username": credentials.username, "role": "user"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def admin_required(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user