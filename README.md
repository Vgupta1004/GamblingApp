# GamblingApp

## UC2: Stake Management Operations

Implements the core betting engine with real-time stake tracking and transaction management.

Supports stake initialization, bet placement, win/loss settlement, deposits, and withdrawals.

Maintains a complete audit trail using `StakeTransaction` records.

Includes boundary validation to detect low/high stake breaches and warnings.

Tracks stake fluctuations using a monitor (peak, lowest, volatility).

Provides detailed reporting with transaction breakdown and net profit/loss.

Supports filtered reports by transaction type.

Ensures consistent balance updates and state tracking across operations.

Run using:

```bash
python main.py
```

