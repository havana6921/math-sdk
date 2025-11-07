"""Gamestate logic for cascade multiplier game."""

from game_override import GameStateOverride


class GameState(GameStateOverride):
    """Handle spin logic and cascading behaviour."""

    def run_spin(self, sim: int, simulation_seed=None):
        self.reset_seed(sim, simulation_seed)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.reveal_board()
            self.process_cascades()
            final_multiplier = self.determine_final_multiplier()
            final_win = self.finish_spin(final_multiplier)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.bonus_multiplier = 0
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs and not self.wincap_triggered:
            self.update_freespin()
            self.reveal_board()
            self.process_cascades()
            final_multiplier = self.determine_final_multiplier(free_game=True)
            self.finish_spin(final_multiplier)
            self.bonus_multiplier = self.global_multiplier

            if self.wincap_triggered:
                break

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()

    def process_cascades(self):
        while not self.wincap_triggered:
            if not self.handle_board_wins():
                break

    def determine_final_multiplier(self, free_game: bool = False) -> int:
        if self.spin_raw_total <= 0:
            if free_game:
                return int(self.global_multiplier)
            return 0
        return int(self.global_multiplier)

    def finish_spin(self, multiplier: int) -> float:
        if self.pending_final_win is not None:
            final_win = self.pending_final_win
        else:
            final_win = self.spin_raw_total * multiplier if multiplier > 0 else 0.0
        final_win = min(final_win, self.config.wincap)

        self.win_manager.set_spin_win(final_win)
        self.emit_final_state(self.spin_raw_total, multiplier, final_win)
        self.win_manager.update_gametype_wins(self.gametype)
        return final_win
