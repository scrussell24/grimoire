from typing import Tuple, List
from dataclasses import dataclass
from functools import wraps

from grimoire import Grimoire

from hype import *


def make_decorator(f):
    '''A simple decorator for creating more decorators'''
    @wraps(f)
    def outter(g):
        @wraps(g)
        def inner(*args, **kwds):
            return f(g, *args, **kwds)
        return inner
    return outter


@dataclass
class State:
    water: int = 0
    ore: int = 0
    organics: int = 0


def template(content: str, state: State, options: List[Option]) -> str:
    return Doc(
      Html(
        Head(
            Style(
'''body {
    background-color: #fefefe;
    color: #222222;
    font-size: 1.5rem;
    font-family: Georgia, 'Times New Roman', Times, serif;
}

ul {
    list-style-type: none;
    padding-left: 0px;
}

li {
    padding-bottom: 1.2rem;
}

a {
    color: #192f50;
    text-decoration: none;
}

.grid {
    display: grid;
    grid-template-areas: 'left content right';
    grid-template-columns: 1fr 3fr 1fr;
}

.grid__content {
    border-width: 1px;
    border-style: solid;
    border-color: #222222;
}

.content_grid {
    display: grid;
    grid-template-areas: 'left right';
    grid-template-columns: 3fr 2fr;
    height: 400px;
}

.content_grid__left {
    padding: 20px;
    background-color: #efefef;
}

.content_grid__right {
    padding: 20px;
    background-color: #222222;
    color: #efefef;
}

.options {
    padding: 20px;
    height: 200px;
}

 @media screen and (max-width: 1000px) {
    .grid {
        grid-template-columns: 0fr 10fr 0fr;
    }

    body {
        font-size: 1.6em;
    }
}'''
            )
        ),
        Body(
          Div(
              Div(_class="grid__left"),
              Div(
                  content,
                  Div(Ul(*[Li(A(o.text, href=f'{o.hash}.html')) for o in options]), _class="options"),
                  _class="grid__content"),
              Div(_class="grid__right"),
              _class="grid")
        )
      )     
    )


@make_decorator
def inventory(fn, state: State) -> Tuple[str, State]:
    content, state = fn(state)
    inv = Ul()
    inv.append(Li(f"Water: {state.water}")) if state.water else ""
    inv.append(Li(f" Ore: {state.ore}")) if state.ore else ""
    inv.append(Li(f" Organics: {state.organics}")) if state.organics else ""
    return Div(
        Div(content, _class="content_grid__left"),
        Div(
            H5(f"Inventory"),
            inv,
            _class="content_grid__right"),
        _class="content_grid"
    ), state


app = Grimoire(state=State, template=template)


@app.start_page
@inventory
def start(state: State) -> Tuple[str, State]:
    state = State()
    return Div(
        P("You have crash landed on an alien planet."),
        P("To fix your spaceship and escape, you need to scavenge three resources from the planet's surface: water, ore, and organic material."),
        P("You stand facing west and see a vast ocean. Turning clockwise, you gaze up at the rising peaks of a mountain range to the north. Continuing east, a forest of tree like structures stretches to the horizon and transitions into a lifeless desert to the south.")
    ), state
    

@app.option(start, "Head west")
@inventory
def west(state: State) -> Tuple[str, State]:
    state.water = 1
    return Div(
        P("You stand on the beach of a large ocean. You notice the lack of waves. No moon, you think"),
        P("You collect water.")
    ), state


@app.option(start, "Head north")
@inventory
def north(state: State) -> Tuple[str, State]:
    state.ore = 1
    return Div(
        P("You head north and find yourself at the foothills of the mountains."),
        P("You find a metalic mineral and mine ore.")
    ), state


@app.option(start, "Head east")
@inventory
def east(state: State) -> Tuple[str, State]:
    state.organics = 1
    return Div(
        P("You head east, towards what looks like a temperate forest. These aren't quite trees, but they almost certainly qualifiy as life and provide a nice shade from the midday sun."),
        P("You extract a sap like substance from the structures. It's a perfect substitute for the organic molecules you are looking for.")
    ), state


@app.option(start, "Head south")
@inventory
def south(state):
    return Div(
        P("You head south towards the lifeless desert. You take the last swig of water from your canteen and collapse to the sand. There's no way you can make it back to your ship. You have died.")
    ), state


@app.option(west, "Head back to the landing site")
@app.option(north, "Head back to the landing site")
@app.option(east, "Head back to the landing site")
@inventory
def landing_site(state: State) -> Tuple[str, State]:
    if (state.water and state.ore and state.organics):
        return Div(
            P("You have all of the materials you need to fix your ship."),
            P("After hours of work, you are ready to take off."),
            P("Good luck traveller.")
        ), state

    return Div(
        P("You arrive back at the crash site. You survey your ship. You still don't have the parts to fix it.")
    ), state


app.option(south, "Start Over")(start)
app.option(landing_site, "Head west", condition=lambda s: not s.water or not s.ore or not s.organics)(west)
app.option(landing_site, "Head north", condition=lambda s: not s.water or not s.ore or not s.organics)(north)
app.option(landing_site, "Head east", condition=lambda s: not s.water or not s.ore or not s.organics)(east)
app.option(landing_site, "Head south", condition=lambda s: not s.water or not s.ore or not s.organics)(south)
app.option(landing_site, "Play again", condition=lambda s: s.water and s.ore and s.organics)(start)


if __name__ == '__main__':
    app.render()
