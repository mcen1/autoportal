from pydantic import BaseModel, Field


class User(BaseModel):
    """
    The POST data the user must send.
    """
    username: str
    password: str


class LoginResponse(BaseModel):
    """
    Final data sent back to the end user.
    """
    access_token: str = Field(default=None, title="Access token provide back to the end user.")


class TokenResponse(BaseModel):
    """
    Token endpoint response.
    """
    result: str = Field(default='Your token is still valid.', title='Information on whether the token is valid or not.')
    expires_in: int = Field(default=0, title='Expiration date in unix epoch.')
    ttl: float = Field(default=0, title='Time remaining before expiring.')
