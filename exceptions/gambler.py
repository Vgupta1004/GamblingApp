from exceptions.base import AppException

class GamblerNotFound(AppException):
    pass

class InvalidStake(AppException):
    pass

class ThresholdError(AppException):
    pass