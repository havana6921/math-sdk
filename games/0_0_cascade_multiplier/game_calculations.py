"""Helper calculations for cascade multiplier game."""

from src.executables.executables import Executables
from src.calculations.scatter import Scatter


class GameCalculations(Executables):
    """Game specific helper methods."""

    def evaluate_scatter_wins(self):
        """Evaluate scatter-style wins without applying global multiplier."""
        self.win_data = Scatter.get_scatterpay_wins(self.config, self.board, global_multiplier=1)
        Scatter.record_scatter_wins(self)
        return self.win_data

    def removed_symbol_positions(self):
        """Return list of positions removed during the latest tumble."""
        removed = []
        for win in self.win_data["wins"]:
            for pos in win["positions"]:
                removed.append({"reel": pos["reel"], "row": pos["row"] + 1})
        removed.sort(key=lambda item: (item["reel"], item["row"]))
        return removed

    def update_scatter_tracking(self):
        """Store highest scatter count and their positions for trigger events."""
        current_positions = self.special_syms_on_board.get("scatter", [])
        current_count = len(current_positions)
        if current_count > self.max_scatter_count:
            self.max_scatter_count = current_count
            self.scatter_positions_for_trigger = [dict(pos) for pos in current_positions]
