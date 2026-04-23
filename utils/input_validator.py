from exceptions.validation_exception import *
from model.validation_result import ValidationResult
from model.validation_config import ValidationConfig
import math


class InputValidator:

    config = ValidationConfig()

    @staticmethod
    def validate_initial_stake(value):
        result = ValidationResult()

        try:
            if value is None:
                raise StakeValidationException(
                    "Stake cannot be null",
                    ValidationErrorType.NULL_ERROR,
                    "stake",
                    value
                )

            if not isinstance(value, (int, float)):
                raise StakeValidationException(
                    "Invalid numeric input",
                    ValidationErrorType.NUMERIC_ERROR,
                    "stake",
                    value
                )

            if math.isnan(value) or math.isinf(value):
                raise StakeValidationException(
                    "Stake cannot be NaN or Infinity",
                    ValidationErrorType.NUMERIC_ERROR,
                    "stake",
                    value
                )

            if value <= 0:
                raise StakeValidationException(
                    "Stake must be positive",
                    ValidationErrorType.STAKE_ERROR,
                    "stake",
                    value
                )

            if value < InputValidator.config.min_stake or value > InputValidator.config.max_stake:
                raise StakeValidationException(
                    "Stake out of allowed range",
                    ValidationErrorType.RANGE_ERROR,
                    "stake",
                    value
                )

        except ValidationException as e:
            result.add_error(e)

        return result
    

    @staticmethod
    def validate_bet_amount(bet, stake):

        result = ValidationResult()

        try:
            if bet <= 0:
                raise BetValidationException(
                    "Bet must be positive",
                    ValidationErrorType.BET_ERROR,
                    "bet",
                    bet
                )

            if bet > stake:
                raise BetValidationException(
                    "Bet exceeds current stake",
                    ValidationErrorType.BET_ERROR,
                    "bet",
                    bet
                )

        except ValidationException as e:
            result.add_error(e)

        return result
    
    @staticmethod
    def validate_probability(p):

        result = ValidationResult()

        try:
            if not (0 <= p <= 1):
                raise ProbabilityValidationException(
                    "Probability must be between 0 and 1",
                    ValidationErrorType.PROBABILITY_ERROR,
                    "probability",
                    p
                )

        except ValidationException as e:
            result.add_error(e)

        return result
    
    @staticmethod
    def validate_limits(lower, upper):

        result = ValidationResult()

        try:
            if upper <= lower:
                raise LimitValidationException(
                    "Upper limit must be greater than lower limit",
                    ValidationErrorType.LIMIT_ERROR,
                    "limits",
                    (lower, upper)
                )

        except ValidationException as e:
            result.add_error(e)

        return result
    
    @staticmethod
    def parse_and_validate_numeric(value, field_name="value"):

        result = ValidationResult()

        try:
            if value is None or value == "":
                raise ValidationException(
                    f"{field_name} cannot be empty",
                    ValidationErrorType.NULL_ERROR,
                    field_name,
                    value
                )

            # try parsing
            parsed = float(value)

            if math.isnan(parsed) or math.isinf(parsed):
                raise ValidationException(
                    f"{field_name} cannot be NaN or Infinity",
                    ValidationErrorType.NUMERIC_ERROR,
                    field_name,
                    value
                )

            return parsed, result

        except ValueError:
            result.add_error(
                ValidationException(
                    f"Invalid number format for {field_name}",
                    ValidationErrorType.NUMERIC_ERROR,
                    field_name,
                    value
                )
            )

        except ValidationException as e:
            result.add_error(e)

        return None, result