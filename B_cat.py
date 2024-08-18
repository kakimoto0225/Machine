import math
import streamlit as st
import pandas as pd

INNINGS_PER_GAME: int = 9

def get_user_input() -> tuple[int, int, int]:
    """ユーザーから入力を取得する"""
    st.title("勝率推定式の一覧")
    runs: int = st.number_input("得点", min_value=1, value=1, step=1)
    runs_allowed: int = st.number_input("失点", min_value=1, value=1, step=1)
    game_count: int = st.number_input("試合数", min_value=1, value=1, step=1)
    return runs, runs_allowed, game_count

def calculate_stats(runs: int, runs_allowed: int, game_count: int) -> tuple[float, float, float, float, float, float]:
    """統計値を計算する"""
    runs_average: float = runs / game_count
    runs_allowed_average: float = runs_allowed / game_count
    average_runs_per_inning: float = runs_average / INNINGS_PER_GAME
    average_runs_allowed_per_inning: float = runs_allowed_average / INNINGS_PER_GAME
    runs_difference: float = abs(runs_average - runs_allowed_average)
    runs_per_game: float = (runs + runs_allowed) / game_count
    return runs_average, runs_allowed_average, average_runs_per_inning, average_runs_allowed_per_inning, runs_difference, runs_per_game

def Cook(runs: int, runs_allowed: int) -> float:
    """Cookの勝率推定式"""
    return 0.484 * (runs / runs_allowed)

def Soolman(runs_average: float, runs_allowed_average: float) -> float:
    """Soolmanの勝率推定式"""
    return (0.102 * runs_average) - (0.103 * runs_allowed_average) + 0.505

def James_2(runs: int, runs_allowed: int) -> float:
    """James 2の勝率推定式"""
    return runs ** 2 / (runs ** 2 + runs_allowed ** 2)

def James_183(runs: int, runs_allowed: int) -> float:
    """James 1.83の勝率推定式"""
    return runs ** 1.83 / (runs ** 1.83 + runs_allowed ** 1.83)

def Pythagenport(runs: int, runs_allowed: int, runs_per_game: float) -> float:
    """Pythagenportの勝率推定式"""
    multiplier: float = 1.50 * math.log(runs_per_game) + 0.45
    return runs ** multiplier / (runs ** multiplier + runs_allowed ** multiplier)

def Pythagenpat(runs: int, runs_allowed: int, runs_per_game: float) -> float:
    """Pythagenpatの勝率推定式"""
    multiplier: float = runs_per_game ** 0.28
    return runs ** multiplier / (runs ** multiplier + runs_allowed ** multiplier)

def Palmer_RPW(average_runs_per_inning: float, average_runs_allowed_per_inning: float) -> float:
    """Palmer RPWの勝率推定式"""
    return 10 * math.sqrt(average_runs_per_inning + average_runs_allowed_per_inning)

def Tango_RPW(runs_per_game: float) -> float:
    """Tango RPWの勝率推定式"""
    return (0.75 * runs_per_game) + 3

def Tango_RPW_RD(runs_per_game: float, runs_difference: float) -> float:
    """Tango RPW RDの勝率推定式"""
    return (0.8 * runs_per_game) + 0.4 * runs_difference + 3

def main() -> None:
    """メイン処理"""
    runs, runs_allowed, game_count = get_user_input()
    runs_average, runs_allowed_average, average_runs_per_inning, average_runs_allowed_per_inning, runs_difference, runs_per_game = calculate_stats(runs, runs_allowed, game_count)

    results: dict[str, list[str | float]] = {
        "Method": ["Cook", "Soolman", "James_2", "James_183", "Pythagenport", "Pythagenpat", "Palmer_RPW", "Tango_RPW", "Tango_RPW_RD"],
        "Winning Rate": [
            Cook(runs, runs_allowed),
            Soolman(runs_average, runs_allowed_average),
            James_2(runs, runs_allowed),
            James_183(runs, runs_allowed),
            Pythagenport(runs, runs_allowed, runs_per_game),
            Pythagenpat(runs, runs_allowed, runs_per_game),
            Palmer_RPW(average_runs_per_inning, average_runs_allowed_per_inning),
            Tango_RPW(runs_per_game),
            Tango_RPW_RD(runs_per_game, runs_difference)
        ]
    }

    df: pd.DataFrame = pd.DataFrame(results)
    st.table(df)

if __name__ == "__main__":
    main()