# Base import
from pydantic import BaseModel


# A settings class for AuthJWT to use
class Settings(BaseModel):
    authjwt_algorithm: str = "RS256"
#    authjwt_private_key: str = JWT_PRIVATE_KEY
#    authjwt_public_key: str = JWT_PUBLIC_KEY
    authjwt_access_token_expires: int = 28800
