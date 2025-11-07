"""Custom event helpers for cascade multiplier game."""

from src.events.events import json_ready_sym


def _board_snapshot(gamestate):
    special_attributes = list(gamestate.config.special_symbols.keys())
    board = []
    for reel, _ in enumerate(gamestate.board):
        column = []
        if gamestate.config.include_padding:
            column.append(json_ready_sym(gamestate.top_symbols[reel], special_attributes))
        for row in range(len(gamestate.board[reel])):
            column.append(json_ready_sym(gamestate.board[reel][row], special_attributes))
        if gamestate.config.include_padding:
            column.append(json_ready_sym(gamestate.bottom_symbols[reel], special_attributes))
        board.append(column)
    return board


def initial_drop_event(gamestate):
    event = {
        "index": len(gamestate.book.events),
        "type": "initialDrop",
        "board": _board_snapshot(gamestate),
        "gameType": gamestate.gametype,
        "multiplier": int(gamestate.global_multiplier),
    }
    gamestate.book.add_event(event)


def animation_event(gamestate):
    wins = []
    for win in gamestate.win_data["wins"]:
        win_copy = {
            "symbol": win["symbol"],
            "amount": round(win["win"], 4),
            "positions": [],
        }
        for pos in win["positions"]:
            win_copy["positions"].append({"reel": pos["reel"], "row": pos["row"] + 1})
        wins.append(win_copy)
    event = {
        "index": len(gamestate.book.events),
        "type": "symbolAnimation",
        "wins": wins,
    }
    gamestate.book.add_event(event)


def clear_and_multiply_event(gamestate, removed_positions, multiplier, base_total):
    event = {
        "index": len(gamestate.book.events),
        "type": "clearAndMultiply",
        "removed": removed_positions,
        "multiplier": int(multiplier),
        "baseWin": round(base_total, 4),
    }
    gamestate.book.add_event(event)


def symbols_drop_event(gamestate):
    event = {
        "index": len(gamestate.book.events),
        "type": "symbolsDrop",
        "board": _board_snapshot(gamestate),
    }
    gamestate.book.add_event(event)


def final_multiplier_win_event(gamestate, base_total, multiplier, final_win):
    event = {
        "index": len(gamestate.book.events),
        "type": "finalWinDetail",
        "baseWin": round(base_total, 4),
        "multiplier": int(multiplier),
        "totalWin": round(final_win, 4),
    }
    gamestate.book.add_event(event)
