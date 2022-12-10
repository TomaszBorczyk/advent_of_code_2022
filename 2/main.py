from enum import Enum
import dataclasses


class RPS(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


@dataclasses.dataclass
class Rule:
    wins_with: RPS
    loses_to: RPS


RULES = {
    RPS.Rock.name: Rule(wins_with=RPS.Scissors, loses_to=RPS.Paper),
    RPS.Scissors.name: Rule(wins_with=RPS.Paper, loses_to=RPS.Rock),
    RPS.Paper.name: Rule(wins_with=RPS.Rock, loses_to=RPS.Scissors)
}


class Outcome(Enum):
    Loss = 0
    Draw = 3
    Win = 6


SIGN_MAPPER = {
    'X': RPS.Rock,
    'Y': RPS.Paper,
    'Z': RPS.Scissors,
    'A': RPS.Rock,
    'B': RPS.Paper,
    'C': RPS.Scissors
}

DESIRED_OUTCOME = { 
    'X': Outcome.Loss,
    'Y': Outcome.Draw,
    'Z': Outcome.Win
}


def get_sign(input: str) -> RPS:
    return SIGN_MAPPER.get(input)


def get_sign_for_desired_outcome(enemy: RPS, outcome: Outcome) -> RPS:
    if outcome == Outcome.Draw:
        return enemy

    if outcome == Outcome.Win:
        return RULES.get(enemy.name).loses_to

    if outcome == Outcome.Loss:
        return RULES.get(enemy.name).wins_with


def get_round_outcome(enemy: RPS, player: RPS) -> Outcome:
    if enemy == RPS.Rock and player == RPS.Scissors:
        return Outcome.Loss

    if enemy == RPS.Scissors and player == RPS.Rock:
        return Outcome.Win

    diff = player.value - enemy.value

    if diff > 0:
        return Outcome.Win
    elif diff == 0:
        return Outcome.Draw
    else:
        return Outcome.Loss


def get_round_input(round):
    return round.split(' ')


def calculate_round_score(enemy: RPS, player: RPS) -> int:
    outcome = get_round_outcome(enemy, player)
    print(f"player_sign: {player.name}/{player.value}, outcome_value: {outcome.name}/{outcome.value}")
    return player.value + outcome.value


def game_score():
    game = open("input.txt", "r", encoding="utf-8")
    total = 0

    for round in game:
        inputs = get_round_input(round.strip())
        enemy = get_sign(inputs[0])
#        player = get_sign(inputs[1])
        desired = DESIRED_OUTCOME.get(inputs[1])
        player = get_sign_for_desired_outcome(enemy, desired)
        score = calculate_round_score(enemy, player)
        total += score

    return total

if __name__ == "__main__":
    score = game_score()
    print(score)
