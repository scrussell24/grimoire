from typing import Tuple
from dataclasses import dataclass

from grimoire import Grimoire, Page

from hype import *


@dataclass
class State:
    day: str = None
    sticks: int = 0


def template(text: str, state: State, option_links: Tuple[str, Page]):
        return Doc(
            Html(
                Body(
                    P(text),
                    Ul(*[Li(A(o.option_text, href=f'{l}.html')) for l, o in option_links])
                )
            )     
        )




app = Grimoire(template, state_class=State)


@app.start_page
def start_page(state):
    state.day = 0
    state.sticks = 0
    return f'you have arrived on a desolate planet. Day {state.day}. Stick {state.sticks}.', state


@app.option(start_page, "go north")
def north(state):
    state.day += 1
    return f'You have travelled north, it took you one day. Day {state.day}. Stick {state.sticks}.', state


@app.option(start_page, "go south")
def south(state):
    state.day += 1
    return f'You have travelled south, it took you one day. Day {state.day}. Stick {state.sticks}.', state


@app.option(start_page, "go east")
def east(state):
    state.day += 1
    return f'You have travelled east, it took you one day. Day {state.day}. Stick {state.sticks}.', state


@app.option(start_page, "go west")
def west(state):
    if state.day < 10:
        state.day += 1
    return f'You have travelled west, it took you one day. Day {state.day}. Stick {state.sticks}.', state


@app.redirect(west)
@app.option(west, 'pick up a stick', lambda s: s.sticks < 10)
def pick_up_stick(state):
    state.sticks += 1
    return '', state

app.option(north, 'start over (n)')(start_page)
app.option(south, 'start over (s)')(start_page)
app.option(east, 'start over (e)')(start_page)
app.option(west, 'start over (w)')(start_page)


if __name__ == '__main__':
    app.render()
