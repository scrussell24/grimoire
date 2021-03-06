from dataclasses import dataclass
from enum import Enum
from random import choice as rchoice
from typing import Callable, List, Optional, Tuple

from hype import Div, Element, P

from grimoire import Grimoire
from grimoire.templates import default_page, link
from grimoire.utils import make_decorator


class Choice(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


@dataclass
class State:
    round: int = 0
    wins: int = 0
    choice: Optional[Choice] = None


page = default_page("Rock, Paper, Scissors")


app = Grimoire(State)


@app.page(start=True)
@page
def begin(state: State, rock: str, paper: str, scissors: str) -> Tuple[Element, List[Tuple[str, str]], State]:

    if state.round < 10:
        state.round += 1

    if state.round >= 10:
        return "Game Over", [], state

    return (
        Div(
            P(f"Round: {state.round} Wins: {state.wins}"),
            P(
                f'Choose {link("rock", rock)}, {link("paper", paper)}, or {link("scissors", scissors)}.'
            ),
        ),
        [("Choose Rock", rock), ("Choose Paper", paper), ("Choose Scissors", scissors)],
        state,
    )


@make_decorator
@page
def choice(f: Callable, state: State, begin: str) -> Tuple[Element, List[Tuple[str, str]], State]:
    state = f(state, begin)
    choice = state.choice
    op_choice = rchoice(list(Choice))

    if choice == Choice.PAPER:
        if op_choice == Choice.ROCK:
            status = "win"
            state.wins += 1
        elif choice == op_choice:
            status = "draw"
        else:
            status = "lose"
    elif choice == Choice.ROCK:
        if op_choice == Choice.SCISSORS:
            status = "win"
            state.wins += 1
        elif choice == op_choice:
            status = "draw"
        else:
            status = "lose"
    else:  # scissors
        if op_choice == Choice.PAPER:
            status = "win"
            state.wins += 1
        elif choice == op_choice:
            status = "draw"
        else:
            status = "lose"

    state.choice = None
    return (
        P(
            f"You chose {choice.value if choice else ''}. Opponent chose {op_choice.value}. You {status}"
        ),
        [("Play another round", begin)],
        state,
    )


@app.page()
@choice
def rock(state: State, begin: str) -> State:
    state.choice = Choice.ROCK
    return state


@app.page()
@choice
def paper(state: State, begin: str) -> State:
    state.choice = Choice.PAPER
    return state


@app.page()
@choice
def scissors(state: State, begin: str) -> State:
    state.choice = Choice.SCISSORS
    return state


if __name__ == "__main__":
    app.render("docs/rps/")
