class PluggyAPIError(Exception):
    """
    Base exception for any Pluggy API error (non-2xx).
    """
    pass

class GlobalErrorResponse(PluggyAPIError):
    """
    Represents Pluggy's GlobalErrorResponse schema:
    """
    def __init__(self, code: int, code_description: str, message: str):
        super().__init__(message)
        self.code = code
        self.code_description = code_description
        self.message = message

class BadRequestError(GlobalErrorResponse):
    """Raised when HTTP 400 occurs."""
    pass

class UnauthorizedError(GlobalErrorResponse):
    """Raised when HTTP 401 occurs (invalid credentials, disabled client, etc.)."""
    pass

class NotFoundError(GlobalErrorResponse):
    """Raised when HTTP 404 occurs (item, account, or other resource not found)."""
    pass

class ConflictError(GlobalErrorResponse):
    """Raised when HTTP 409 occurs (e.g. item creation limit, updating before allowed frequency)."""
    pass

class InternalServerError(GlobalErrorResponse):
    """Raised when HTTP 500 occurs."""
    pass
