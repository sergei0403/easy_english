from pydantic import (
    BaseModel,
    model_validator,
)


class RegisterSchema(BaseModel):
    email: str
    login: str
    first_name: str
    last_name: str
    password: str
    r_password: str

    @model_validator(mode='before')
    @classmethod
    def verify_password_match(cls, values: dict) -> dict:
        if values.get('password') != values.get('r_password'):
            raise ValueError('The passwords and r_password must be the same.')
        return values


class LoginSchema(BaseModel):
    email: str
    password: str


class RefreshTokenSchema(BaseModel):
    token: str


class AuthenticatedUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    token: str
