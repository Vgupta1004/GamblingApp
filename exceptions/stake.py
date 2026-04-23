from .base import ValidationException

class StakeError(ValidationException):
    def __init__(self, message):
        super().__init__(message, error_type="STAKE_ERROR")