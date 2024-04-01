from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse

from app.dependencies.auth import get_current_user
from schemas.auth_schemas import RegisterSchema, LoginSchema, RefreshTokenSchema, AuthenticatedUser
from services.user_service import UserDBService
from storages.jwt_token_storage import StoreTokenRedis
from utils.password import get_hashed_password, verify_password
from utils.jwt_token import decode_token, check_expired_token

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/sign_up/', summary='Create new user')
async def sign_up(user_item: RegisterSchema):
    user_service = UserDBService()
    user = await user_service.get_user_by_email(email=user_item.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exist'
        )
    coded_password = get_hashed_password(user_item.password)
    user_item.password = coded_password
    user_item.r_password = coded_password
    await user_service.create_user(user_item=user_item)
    user = await user_service.get_user_by_email(email=user_item.email)
    token_storage = StoreTokenRedis()
    token, _ = token_storage.create(user=user)
    return {
        'access_token': token.access,
        'refresh_token': token.refresh,
    }


@auth_router.post('/sign_in/', summary='Login in system')
async def sign_in(data: LoginSchema):
    user_service = UserDBService()
    user = await user_service.get_user_by_email(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email doesn`t exist'
        )
    if not verify_password(password=data.password, hashed_pass=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong password'
        )
    token_storage = StoreTokenRedis()
    token, _ = token_storage.create(user=user)
    return {
        'access_token': token.access,
        'refresh_token': token.refresh,
    }


@auth_router.post('/refresh_token/')
async def refresh_token(data: RefreshTokenSchema):
    decoded_token = decode_token(data.token)
    if check_expired_token(decoded_token.get('date_exp')):
        token_storage = StoreTokenRedis()
        token, _ = await token_storage.update(jti=decoded_token.get('jti'))
        return {
            'access_token': token.access,
            'refresh_token': token.refresh,
        }
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This token was expired'
        )


@auth_router.get('/me/', summary='Get details of currently logged in user', response_model=AuthenticatedUser)
async def get_me(user: AuthenticatedUser = Depends(get_current_user)):
    return user
