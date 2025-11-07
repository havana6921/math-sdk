import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Configuration for the cascade multiplier scatter game."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_cascade_multiplier"
        self.game_name = "cascade_multiplier"
        self.provider_numer = 0
        self.working_name = "Cascade Multiplier Scatter"
        self.wincap = 5000.0
        self.win_type = "scatter"
        self.rtp = 0.9650
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 6
        self.num_rows = [5] * self.num_reels

        # Paytable definition
        ranges = ((8, 9), (10, 12), (13, 30))
        symbols = {
            "S1": (0.1, 1.5, 4.0),
            "S2": (0.1, 1.5, 4.0),
            "S3": (0.2, 2.5, 5.0),
            "S4": (0.4, 3.5, 8.0),
            "S5": (0.6, 4.0, 10.0),
            "S6": (1.0, 6.0, 20.0),
            "S7": (1.3, 7.0, 30.0),
            "S8": (2.0, 10.0, 40.0),
            "S9": (3.0, 15.0, 60.0),
        }
        pay_group = {}
        for sym, pays in symbols.items():
            for rng, amount in zip(ranges, pays):
                pay_group[(rng, sym)] = amount
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = True
        self.special_symbols = {"wild": [], "scatter": ["SC"], "multiplier": []}

        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 12, 5: 15, 6: 20},
            self.freegame_type: {3: 10, 4: 12, 5: 15, 6: 20},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for key, filename in reels.items():
            self.reels[key] = self.read_reels_csv(os.path.join(self.reels_path, filename))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {6: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.12,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {3: 8, 4: 2, 5: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.38,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.489,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {self.freegame_type: {"FR0": 1}},
                            "scatter_triggers": {3: 10, 4: 3, 5: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    )
                ],
            ),
        ]
