# GamblingApp

## UC4: Game Session Management

Implements a complete session lifecycle for gambling with start, pause, resume, and end states.

Supports automatic session termination based on upper (win) and lower (loss) stake limits.

Tracks real-time gameplay with continuous boundary validation after each bet.

Includes pause/resume functionality with full pause history and duration tracking.

Separates total session time into active play time and paused time.

Records each game using GameRecord for detailed audit and analysis.

Provides session-level statistics including total profit, win rate, average bet, and ROI.

Manages multiple sessions using GameSessionManager with active and completed session tracking.

Ensures robust control flow with safe handling of session states and transitions.

