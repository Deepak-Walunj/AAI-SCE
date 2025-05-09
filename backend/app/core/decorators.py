from typing import List, Optional, Callable, Any, TypeVar
from typing_extensions import ParamSpec
from functools import wraps
from fastapi import Request, HTTPException, status, Depends
from fastapi.security.utils import get_authorization_scheme_param
from .exceptions import ForbiddenException
from ..core.config import settings
from app.services.auth import AuthService
from app.api.deps import get_auth_service
from app.core.database import database
from app.core.collections import CollectionName
from app.core.exceptions import AppException

P = ParamSpec("P")
R = TypeVar("R")

def allowed_entities(entity_types: Optional[List[str]] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to check if a user is allowed to access the route based on their entity type."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(request: Request, *args: P.args, **kwargs: P.kwargs) -> R:
            try:
                # Ensure database connection is established
                # await database.connect()
                
                # Get auth service using dependency injection
                auth_service = get_auth_service()

                # Get token from either cookie or header based on env
                token = None
                if settings.USE_COOKIE_AUTH:
                    token = request.cookies.get('access_token')
                else:
                    authorization = request.headers.get("Authorization")
                    if authorization:
                        scheme, token = get_authorization_scheme_param(authorization)
                        if scheme.lower() != "bearer":
                            token = None
                if not token:
                    # If no token, check if this is a public route
                    if entity_types is not None:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"}
                        )
                    return await func(request, *args, **kwargs)

                # Get auth service using dependency injection
                auth_service = get_auth_service()
                
                # Verify token
                payload = await auth_service.verify_token(token)
                if not payload:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token",
                        headers={"WWW-Authenticate": "Bearer"}
                    )

                # Get user from auth service
                user_id = payload.get("sub")
                if not user_id:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token payload",
                        headers={"WWW-Authenticate": "Bearer"}
                    )

                user = await auth_service.get_user_by_id(user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not found",
                        headers={"WWW-Authenticate": "Bearer"}
                    )

                # Check entity type if specified
                if entity_types and user.entity_type not in entity_types:
                    raise ForbiddenException("You don't have permission to access this resource")

                # Store payload and user in request state
                request.state.auth_payload = payload
                request.state.user = user
            except ForbiddenException as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e)
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e),
                    headers={"WWW-Authenticate": "Bearer"}
                )
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator