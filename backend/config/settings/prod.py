from .base import *  # noqa: F403
from .base import env

DEBUG = False
if SECRET_KEY == "insecure-dev-key":  # noqa: F405
    raise RuntimeError("DJANGO_SECRET_KEY must be set in production.")

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", "true").lower() == "true"
