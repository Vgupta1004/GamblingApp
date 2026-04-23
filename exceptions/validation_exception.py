from enum import Enum


class ValidationErrorType(Enum):
    STAKE_ERROR = "STAKE_ERROR"
    BET_ERROR = "BET_ERROR"
    LIMIT_ERROR = "LIMIT_ERROR"
    PROBABILITY_ERROR = "PROBABILITY_ERROR"
    NUMERIC_ERROR = "NUMERIC_ERROR"
    RANGE_ERROR = "RANGE_ERROR"
    NULL_ERROR = "NULL_ERROR"

class ValidationException(Exception):

    def __init__(self, message, error_type, field=None, value=None):
        super().__init__(message)
        self.error_type = error_type
        self.field = field
        self.value = value

class StakeValidationException(ValidationException):
    pass


class BetValidationException(ValidationException):
    pass


class LimitValidationException(ValidationException):
    pass


class ProbabilityValidationException(ValidationException):
    pass