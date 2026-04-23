# GamblingApp

## UC3: Betting Mechanism

Implements the core betting engine with probability-based outcomes and automated stake updates.

Supports single bet placement with validation against available balance.

Determines win/loss using configurable probabilities and calculates winnings via odds.

Integrates with StakeService to handle deductions and settlements.

Implements multiple betting strategies (Fixed, Percentage, Martingale).

Supports consecutive bets through session-based execution.

Tracks each bet with full details including amount, outcome, and balance changes.

Provides session summaries with win rate, total bets, and profit/loss.

Ensures robust error handling for insufficient balance and invalid bets.
