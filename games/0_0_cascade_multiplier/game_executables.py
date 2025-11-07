"""Game specific executable helpers."""

from game_calculations import GameCalculations
from game_events import (
    initial_drop_event,
    animation_event,
    clear_and_multiply_event,
    symbols_drop_event,
    final_multiplier_win_event,
)
from src.events.events import (
    set_total_event,
    set_win_event,
    wincap_event,
    update_freespin_event,
)


class GameExecutables(GameCalculations):
    """Bundle small reusable helpers for the cascade multiplier slot."""

    def reveal_board(self):
        """Draw the current board and emit initial drop event."""
        super().draw_board(emit_event=False)
        self.update_scatter_tracking()
        initial_drop_event(self)

    def update_freespin(self) -> None:
        """Update free spin counters without resetting the persistent multiplier."""
        update_freespin_event(self)
        self.fs += 1
        self.win_manager.reset_spin_win()
        self.win_data = {}
        self.spin_raw_total = 0.0
        self.pending_final_win = None
        self.max_scatter_count = 0
        self.scatter_positions_for_trigger = []
        self.global_multiplier = self.bonus_multiplier
        self.win_manager.tumble_win = 0.0

    def tumble_and_emit(self):
        """Apply tumble logic and send the board update event."""
        self.tumble_board()
        self.update_scatter_tracking()
        symbols_drop_event(self)

    def emit_final_state(self, base_total: float, multiplier: int, final_win: float):
        """Emit end of spin events."""
        if final_win > 0:
            set_win_event(self)
        set_total_event(self)
        final_multiplier_win_event(self, base_total, multiplier, final_win)
        if self.wincap_triggered:
            wincap_event(self)

    def handle_board_wins(self):
        """Evaluate wins on current board and emit relevant events."""
        self.evaluate_scatter_wins()
        if self.win_data["totalWin"] <= 0:
            return False

        animation_event(self)

        clusters = len(self.win_data["wins"])
        self.spin_raw_total += self.win_data["totalWin"]
        self.win_manager.tumble_win = self.spin_raw_total
        self.global_multiplier += clusters

        removed_positions = self.removed_symbol_positions()
        clear_and_multiply_event(
            self,
            removed_positions,
            self.global_multiplier,
            self.spin_raw_total,
        )

        potential_win = self.spin_raw_total * self.global_multiplier if self.spin_raw_total > 0 else 0
        if potential_win >= self.config.wincap:
            self.wincap_triggered = True
            self.pending_final_win = self.config.wincap
            return False

        self.tumble_and_emit()
        return True
