"""Optimization configuration for cascade multiplier game."""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructFenceBias,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Provide optimization presets for base and bonus modes."""

    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=5000, search_conditions=5000).return_dict(),
                    "0": ConstructConditions(rtp=0.0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(rtp=0.4, hr=180, search_conditions={"symbol": "scatter"}).return_dict(),
                    "basegame": ConstructConditions(rtp=0.55, hr=4.0).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "basegame", "scale_factor": 1.2, "win_range": (2, 5), "probability": 1.0},
                        {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 25), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.85, "win_range": (200, 400), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.1, "win_range": (800, 1200), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(3.0, 6.0)],
                    bias_weights=[0.5],
                ).return_dict(),
            },
            "bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=5000, search_conditions=5000).return_dict(),
                    "freegame": ConstructConditions(rtp=0.96, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "freegame", "scale_factor": 0.9, "win_range": (30, 80), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.8, "win_range": (400, 800), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.15, "win_range": (2000, 3000), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["freegame"],
                    bias_ranges=[(80.0, 140.0)],
                    bias_weights=[0.3],
                ).return_dict(),
            },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
