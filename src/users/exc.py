from fastapi import HTTPException, status

email_in_use_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already in use"
)

password_invalid_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Wrong current password"
)

password_to_week_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Password to week!"
)
