class ValidationResult:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_error(self, error):
        self.errors.append(str(error))

    def add_warning(self, warning):
        self.warnings.append(warning)

    def is_valid(self):
        return len(self.errors) == 0

    def get_summary(self):
        return {
            "valid": self.is_valid(),
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def has_warnings(self):
        return len(self.warnings) > 0