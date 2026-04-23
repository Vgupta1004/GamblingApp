# GamblingApp

## UC1: Gambler Profile Management

Implements core profile management for gamblers including creation, update, retrieval, validation, and reset operations.

Each gambler stores financial data (initial/current stake, thresholds) along with betting preferences and statistics.

A layered architecture is used:

* `model` for entities
* `services` for business logic
* `dto` for structured outputs
* `config` for database handling

Includes input validation, custom exception handling, and timestamp tracking.

Statistics such as net profit, win rate, and average bet are computed via DTO.

Reset functionality restores initial state with proportional threshold adjustment.

Run using:

```bash
python main.py
```
