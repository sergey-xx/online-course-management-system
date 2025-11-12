import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_user_from_token(token_key):
    User = get_user_model()  # NOQA: N806
    try:
        access_token = AccessToken(token_key)
        user_id = access_token["user_id"]

        return User.objects.get(id=user_id)
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError, User.DoesNotExist):
        return AnonymousUser()
    except Exception:
        return AnonymousUser()


class JWTAuthMiddleware:
    """Middleware, which get JWT from header and set 'user' in scope."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode()
            if auth_header.startswith("Bearer "):
                token_key = auth_header.split(" ")[1]

                if token_key:
                    scope["user"] = await get_user_from_token(token_key)
        if not scope.get("user"):
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):  # NOQA: N802
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
