"""Domain errors raised by services.

They carry no HTTP knowledge; ``core.exception_handler`` maps them to HTTP
responses at the edge of the system.
"""


class DomainError(Exception):
    code = "domain_error"

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(DomainError):
    code = "not_found"


class InvalidQueryError(DomainError):
    code = "invalid_query"
