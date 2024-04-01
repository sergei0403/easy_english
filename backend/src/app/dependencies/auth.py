from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.requests import Request

from schemas.auth_schemas import AuthenticatedUser
from services.user_service import UserDBService
from utils.jwt_token import check_expired_token, decode_token


async def get_current_user(
    request: Request, access_token: str = Depends(HTTPBearer())
) -> AuthenticatedUser:
    decoded_token = decode_token(access_token.credentials)

    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not check_expired_token(decoded_token.get("date_exp")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserDBService()
    user = await user_service.get_user_by_email(email=decoded_token.get("email"))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    request.state.user = AuthenticatedUser(
        token=access_token.credentials, **user.__dict__
    )
    return request.state.user
