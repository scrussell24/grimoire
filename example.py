from typing import *
from dataclasses import dataclass


from grimoire import Grimoire
from grimoire.templates import link
from grimoire.utils import make_decorator

from hype import *


@dataclass
class State:
    water: int = 0
    ore: int = 0
    organics: int = 0


@make_decorator
def base(fn, state: State, *opts: List[int]) -> Tuple[Element, State]:
    content, options, state = fn(state, *opts)
    return (
        Doc(
            Html(
                Head(Style(CSS)),
                Body(
                    Div(
                        Div(_class="grid__left"),
                        Div(
                            content,
                            Div(
                                Ul(*[Li(link(o[0], o[1])) for o in options]),
                                _class="options",
                            ),
                            _class="grid__content",
                        ),
                        Div(_class="grid__right"),
                        _class="grid",
                    )
                ),
            )
        ),
        state,
    )


@make_decorator
def inventory(
    fn, state: State, *opts: List[int]
) -> Tuple[Element, List[Tuple[str, int]], State]:
    content, options, state = fn(state, *opts)
    inv = Ul()
    inv.append(Li(f"Water: {state.water}")) if state.water else ""
    inv.append(Li(f" Ore: {state.ore}")) if state.ore else ""
    inv.append(Li(f" Organics: {state.organics}")) if state.organics else ""
    return (
        Div(
            Div(content, _class="content_grid__left"),
            Div(H5(f"Inventory"), inv, _class="content_grid__right"),
            _class="content_grid",
        ),
        options,
        state,
    )


app = Grimoire(state=State)


@app.page(start=True)
@base
@inventory
def start(
    state: State, west: int, north: int, east: int, south: int
) -> Tuple[Element, List[Tuple[str, int]], State]:
    state = State()
    return (
        Div(
            P("You have crash landed on an alien planet."),
            P(
                "To fix your spaceship and escape, you need to scavenge three resources from the planet's surface: water, ore, and organic material."
            ),
            P(
                f"You stand facing {link('west', west)} and see a vast ocean. Turning clockwise, you gaze up at the rising peaks of a mountain range to the {link('north', north)}. Continuing {link('east', east)}, a forest of tree like structures stretches to the horizon and transitions into a lifeless desert to the {link('south', south)}."
            ),
        ),
        [
            ("Head West", west),
            ("Head North", north),
            ("Head East", east),
            ("Head South", south),
        ],
        state,
    )


@app.page()
@base
@inventory
def west(state: State, landing_site: int) -> Tuple[str, List[Tuple[str, int]], State]:
    state.water = 1
    return (
        Div(
            P(
                "You stand on the beach of a large ocean. You notice the lack of waves. No moon, you think"
            ),
            P("You collect water."),
        ),
        [("Head back to the landing site", landing_site)],
        state,
    )


@app.page()
@base
@inventory
def north(state: State, landing_site: int) -> Tuple[str, List[Tuple[str, int]], State]:
    state.ore = 1
    return (
        Div(
            P("You head north and find yourself at the foothills of the mountains."),
            P("You find a metalic mineral and mine ore."),
        ),
        [("Head back to the landing site", landing_site)],
        state,
    )


@app.page()
@base
@inventory
def east(state: State, landing_site: int) -> Tuple[str, List[Tuple[str, int]], State]:
    state.organics = 1
    return (
        Div(
            P(
                "You head east, towards what looks like a temperate forest. These aren't quite trees, but they almost certainly qualifiy as life and provide a nice shade from the midday sun."
            ),
            P(
                "You extract a sap like substance from the structures. It's a perfect substitute for the organic molecules you are looking for."
            ),
        ),
        [("Head back to the landing site", landing_site)],
        state,
    )


@app.page()
@base
@inventory
def south(state: State, start: int) -> Tuple[str, List[Tuple[str, int]], State]:
    state = State()
    return (
        Div(
            P(
                "You head south towards the lifeless desert. You take the last swig of water from your canteen and collapse to the sand. There's no way you can make it back to your ship. You have died."
            )
        ),
        [("Start Over", start)],
        state,
    )


@app.page()
@base
@inventory
def landing_site(
    state: State, start: int, west: int, north: int, east: int, south: int
) -> Tuple[str, List[Tuple[str, int]], State]:
    if state.water and state.ore and state.organics:
        state = State()
        return (
            Div(
                P("You have all of the materials you need to fix your ship."),
                P("After hours of work, you are ready to take off."),
                P("Good luck traveller."),
            ),
            [("Start Over", start)],
            state,
        )

    return (
        Div(
            P(
                "You arrive back at the crash site. You survey your ship. You still don't have the parts to fix it."
            )
        ),
        [
            ("Head West", west),
            ("Head North", north),
            ("Head East", east),
            ("Head South", south),
        ],
        state,
    )


CSS = """body {
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
    color: #4444aa;
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
}"""


if __name__ == "__main__":
    app.render(path="example/")
