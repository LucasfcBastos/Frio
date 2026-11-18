"""Uniform error envelope for every API response.

    {"error": {"code": "not_found", "message": "...", "details": {...}}}
"""

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.exceptions import DomainError, InvalidQueryError, NotFoundError

_DOMAIN_STATUS = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidQueryError: status.HTTP_400_BAD_REQUEST,
}


def _envelope(code: str, message: str, details: dict | list | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}


def api_exception_handler(exc: Exception, context: dict) -> Response | None:
    if isinstance(exc, DomainError):
        http_status = _DOMAIN_STATUS.get(type(exc), status.HTTP_400_BAD_REQUEST)
        return Response(_envelope(exc.code, exc.message, exc.details), status=http_status)

    response = exception_handler(exc, context)
    if response is None:
        return None  # Unhandled: let Django return a 500.

    if isinstance(exc, ValidationError):
        response.data = _envelope("validation_error", "Invalid request parameters.", exc.detail)
    elif isinstance(exc, APIException):
        response.data = _envelope(exc.default_code, str(exc.detail))
    return response
