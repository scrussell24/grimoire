from enum import Enum
from typing import Optional
from dataclasses import dataclass

from hype import *

from grimoire import Grimoire
from grimoire.utils import make_decorator
from grimoire.templates import default_page, link


class Choice(Enum):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'


@dataclass
class State:
    round: int = 0
    choice: Optional[Choice] = None


page = default_page("RPS")


app = Grimoire(State)


@app.page(start=True)
@page
def begin(state, rock, paper, scissors):

    if state.round <= 10:
        state.round += 1

    if state.round >= 10:
        return 'Game Over', [], state

    return f'Choose {link("rock", rock)}, {link("paper", paper)}, or {link("scissors", scissors)}.', [
        ('Choose Rock', rock),
        ('Choose Paper', paper),
        ('Choose Scissors', scissors)
    ], state


@make_decorator
@page
def choice(f, state, begin):
    state = f(state, begin)
    choice = state.choice
    return f'You chose {choice.value}', [('Start Over', begin)], state


@app.page()
@choice
def rock(state, begin):
    state.choice = Choice.ROCK
    return state


@app.page()
@choice
def paper(state, begin):
    state.choice = Choice.PAPER
    return state


@app.page()
@choice
def scissors(state, begin):
    state.choice = Choice.SCISSORS
    return state


if __name__ == '__main__':
    app.render()
