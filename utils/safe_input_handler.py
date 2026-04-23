from utils.input_validator import InputValidator
class SafeInputHandler:

    @staticmethod
    def get_valid_number(prompt, field_name="value"):

        while True:

            user_input = input(prompt)

            value, result = InputValidator.parse_and_validate_numeric(
                user_input,
                field_name
            )

            if not result.is_valid():
                print("Error:", result.errors)
                continue

            return value
        
    @staticmethod
    def get_valid_stake():
        while True:
            value = SafeInputHandler.get_valid_number("Enter stake: ", "stake")
            result = InputValidator.validate_initial_stake(value)
            if not result.is_valid():
                print("Error:", result.errors)
                continue
            return value
        
    @staticmethod
    def get_valid_probability():
        while True:
            value = SafeInputHandler.get_valid_number("Enter probability (0-1): ", "probability")
            result = InputValidator.validate_probability(value)
            if not result.is_valid():
                print("Error:", result.errors)
                continue
            return value