#!/usr/bin/python3
"""Authentication support."""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
from api.v1.configurations.database import get_db
from api.v1.configurations.settings import settings
from api.v1.models.data.users import User, Trustee
from api.v1.models.schemas.users import TokenData

SECRET_KEY = settings.OAUTH2_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_WEEKS = settings.ACCESS_TOKEN_EXPIRE_WEEKS


class BasicAuth(SecurityBase):
    """Basic authentication."""

    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        """Initialize the authentication."""
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        """Call the given request."""
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated"
                )
            return None
        return param


class OAuth2PasswordBearerCookie(OAuth2):
    """Oauth2 password cookie authentication."""

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        """Initialize a new OAuth2 password cookie."""
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """Call the given request."""
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated"
                )
            return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="login_token")
basic_auth = BasicAuth(auto_error=False)


def create_token(data: dict) -> str:
    """Create a new access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """Verify access token provided by user."""
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = decoded_jwt.get("uuid_pk")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(uuid_pk=user_id)

    except JWTError as exc:
        raise credentials_exception from exc

    return token_data


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_db)
):
    """Get current user helper."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = verify_token(token, credentials_exception)
    query = session.query(User).filter(
        User.uuid_pk == user.uuid_pk
    ).first()
    if query:
        return query
    else:
        trustee = session.query(Trustee).filter(
            Trustee.uuid_pk == user.uuid_pk
        ).first()
        return trustee
