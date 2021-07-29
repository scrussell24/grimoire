from grimoire import Grimoire
from grimoire.templates import link

from hype import *


from dataclasses import dataclass


@dataclass
class State:
    message: str = ""


app = Grimoire(State)


from grimoire.templates import default_page


page = default_page("Minimal Example")


@app.page(start=True)
@page
def start(state, second):
    state.message = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!")
    ), [("Go to the second page", second)], state


@app.page()
@page
def second(state, start):
    return Div(
        P(f"message: {state.message}")
    ), [("Start over", start)], state


if __name__ == "__main__":
    app.render()
