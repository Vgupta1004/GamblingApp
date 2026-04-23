from model.game_result import GameResult
from model.running_totals import RunningTotals
from model.winloss_statistics import WinLossStatistics


class WinLossCalculator:

    @staticmethod
    def process_game(stake, bet_amount, outcome, odds_config, probability):

        stake_before = stake

        if outcome:
            win_amount = odds_config.calculate_win(bet_amount, probability)
            stake_after = stake + (win_amount - bet_amount)
        else:
            win_amount = 0
            stake_after = stake - bet_amount

        result = GameResult(
            bet_amount,
            outcome,
            win_amount,
            stake_before,
            stake_after
        )

        return result, stake_after
    
    @staticmethod
    def run_session(initial_stake, bet_amount, rounds, strategy, odds, probability):

        stake = initial_stake

        totals = RunningTotals(initial_stake)
        stats = WinLossStatistics()

        results = []

        for _ in range(rounds):

            outcome = strategy.determine_outcome(probability)

            result, stake = WinLossCalculator.process_game(
                stake,
                bet_amount,
                outcome,
                odds,
                probability
            )

            totals.update(result)
            stats.update(result)

            results.append(result)

        return {
            "final_stake": stake,
            "net_profit": totals.get_net_profit(),
            "balance_history": totals.balance_history,
            "statistics": stats.get_summary()
        }