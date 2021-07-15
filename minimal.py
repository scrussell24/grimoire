from enum import Enum
from typing import Optional
from functools import wraps
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
    choice: Optional[Choice] = None


default_page = default_page("Minimal Example")


app = Grimoire(State)


@app.page(start=True)
@default_page
def begin(state, rock, paper, scissors):
    return f'Choose {link("rock", rock)}, {link("paper", paper)}, or {link("scissors", scissors)}.', [
        ('Choose Rock', rock),
        ('Choose Paper', paper),
        ('Choose Scissors', scissors)
    ], state


@make_decorator
@default_page
def choice(f, state, begin):
    state = f(state, begin)
    choice = state.choice
    state= State()
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
