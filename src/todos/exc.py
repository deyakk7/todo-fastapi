from fastapi import HTTPException, status

invalid_todo_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found todo with this id",
    headers={"WWW-Authenticate": "Bearer"},
)

not_a_owner_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to do this",
    headers={"WWW-Authenticate": "Bearer"},
)
