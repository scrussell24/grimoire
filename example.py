from typing import Tuple
from dataclasses import dataclass

from grimoire import Grimoire

from hype import *


@dataclass
class State:
    water: bool = False
    ore: bool = False
    organics: bool = False


def getInventoryTemplate(state):
    return Div(P(f"Inventory -- Water: {state.water}, Ore: {state.ore}, Organics: {state.organics}"))


app = Grimoire(state=State)


@app.start_page
def start(state: State) -> Tuple[str, State]:
    state = State()
    return Div(
        P("You have crash landed on an alien planet."),
        P("To fix your spaceship and escape, you need to scavenge three resources from the planet's surface: water, ore, and organic material."),
        P("You stand facing west and see a vast ocean. Turning clockwise, you gaze up at the rising peaks of a mountain range to the north. Continuing east, a forest of tree like structures stretches to the horizon and transitions into a lifeless desert to the south."),
        getInventoryTemplate(state)
    ), state
    

@app.option(start, "Head west")
def west(state: State) -> Tuple[str, State]:
    state.water = True
    return Div(
        P("You stand on the beach of a large ocean. You notice the lack of waves. No moon, you think"),
        P("You collect water."),
        getInventoryTemplate(state)
    ), state


@app.option(start, "Head north")
def north(state: State) -> Tuple[str, State]:
    state.ore = True
    return Div(
        P("You head north and find yourself at the foothills of the mountains."),
        P("You find a metalic mineral and mine ore."),
        getInventoryTemplate(state)
    ), state


@app.option(start, "Head east")
def east(state: State) -> Tuple[str, State]:
    state.organics = True
    return Div(
        P("You head east, towards what looks like a temperate forest. These aren't quite tree, but they almost certainly qualifiy as life and provide a nice shade from the midday sun."),
        P("You extract a sap like substance from the strucutes. It's a perfect substitute for the orgaic molecules you are looking for."),
        getInventoryTemplate(state)
    ), state


@app.option(start, "Head south")
def south(state):
    return Div(
        P("You head south towards the lifeless desert. You take the last swig of water from your canteen and collapse to the sand. There's no way you can make it back to your ship. You have died."),
        getInventoryTemplate(state)
    ), state


@app.option(west, "Head back to the landing site")
@app.option(north, "Head back to the landing site")
@app.option(east, "Head back to the landing site")
def landing_site(state: State) -> Tuple[str, State]:
    if (state.water and state.ore and state.organics):
        return Div(
            P("You have all of the materials you need to fix your ship."),
            P("After hours of work, you are ready to take off."),
            P("Good luck traveller.")
        ), state

    return Div(
        P("You arrive back at the crash site. You survey your ship. You still don't have the parts to fix it."),
        getInventoryTemplate(state)
    ), state

app.option(south, "Start Over")(start)

app.option(landing_site, "Head west", condition=lambda s: not s.water or not s.ore or not s.organics)(west)
app.option(landing_site, "Head north", condition=lambda s: not s.water or not s.ore or not s.organics)(north)
app.option(landing_site, "Head east", condition=lambda s: not s.water or not s.ore or not s.organics)(east)
app.option(landing_site, "Head south", condition=lambda s: not s.water or not s.ore or not s.organics)(south)
app.option(landing_site, "Play again", condition=lambda s: s.water and s.ore and s.organics)(start)


if __name__ == '__main__':
    app.render()
