from fastapi import HTTPException, status

login_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Wrong email or password",
    headers={"WWW-Authenticate": "Bearer"}
)

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"}
)
