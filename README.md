# GamblingApp

## UC6: Input Validation and Error Handling

Implements a robust validation layer to ensure all inputs meet defined constraints and rules.

Includes a custom exception hierarchy for precise error categorization and handling.

Validates stake, bet amounts, probability values, and session limits with strict checks.

Prevents invalid states such as negative stakes, excessive bets, and incorrect boundaries.

Handles invalid numeric inputs (null, strings, NaN, infinity) safely and gracefully.

Provides a ValidationResult system to collect errors and warnings without crashing execution.

Supports configurable validation rules via a centralized ValidationConfig.

Includes SafeInputHandler for interactive input with retry logic and user-friendly feedback.

Ensures system reliability by enforcing data integrity across all modules.
