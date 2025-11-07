"""Override hooks for cascade multiplier game."""

from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    """Override reusable state helpers."""

    def __init__(self, config):
        super().__init__(config)
        self.bonus_multiplier = 0

    def reset_book(self):
        super().reset_book()
        self.spin_raw_total = 0.0
        self.global_multiplier = 0
        self.pending_final_win = None
        self.max_scatter_count = 0
        self.scatter_positions_for_trigger = []
        self.bonus_multiplier = 0

    def reset_fs_spin(self):
        super().reset_fs_spin()
        self.spin_raw_total = 0.0
        self.pending_final_win = None
        self.max_scatter_count = 0
        self.scatter_positions_for_trigger = []
        self.global_multiplier = self.bonus_multiplier

    def assign_special_sym_function(self):
        self.special_symbol_functions = {}

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        original_positions = self.special_syms_on_board.get(scatter_key, [])
        if self.scatter_positions_for_trigger:
            self.special_syms_on_board[scatter_key] = list(self.scatter_positions_for_trigger)
        super().update_freespin_amount(scatter_key=scatter_key)
        self.special_syms_on_board[scatter_key] = original_positions

    def update_fs_retrigger_amt(self, scatter_key: str = "scatter"):
        original_positions = self.special_syms_on_board.get(scatter_key, [])
        if self.scatter_positions_for_trigger:
            self.special_syms_on_board[scatter_key] = list(self.scatter_positions_for_trigger)
        super().update_fs_retrigger_amt(scatter_key=scatter_key)
        self.special_syms_on_board[scatter_key] = original_positions

    def check_fs_condition(self, scatter_key: str = "scatter") -> bool:
        if self.max_scatter_count >= min(self.config.freespin_triggers[self.gametype].keys()) and not self.repeat:
            return True
        return False
