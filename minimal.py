from dataclasses import dataclass

from hype import *

from grimoire import Grimoire, default_template, link


@dataclass
class State:
    rope: bool = False
    axe: bool = False
    torch: bool = False


app = Grimoire(state=State)


default_template = default_template("Minimal Example")


@app.begin
@default_template
def start(state, *opts):
    return '''You\'re adventure has begun. Choose one of the
    following items to help complete your quest.''', state


def update_item(item):
    def updater(state):
        setattr(state, item, True)
        return state
    return updater


@start.option("A rope", update=update_item('rope'))
@start.option("An axe", update=update_item('axe'))
@start.option("A torch", update=update_item('torch'))
@default_template
def choose_item(state, item, boulder):
    if state.rope:
        item_name = 'a rope'
    elif state.axe:
        item_name = 'an axe'
    else:
        item_name = 'a torch'
    return Div(
        P(f"Congratulations, you have chosen {item_name}."),
        P(
            f"""You are standing in front of a deep chasm. You must cross it to
            continue your quest. You feel uneasy as you peer over the edge. 
            To your left you see a large {link(boulder, 'boulder')}. You squint
            and think you might see some writing in it."""
        )
    ), state


@choose_item.option('Use you rope', condition=lambda s: s.rope == True)
@default_template
def use_rope(state, *opts):
    return """You tie rope around the trunk of a dead tree near the edge
    of the chasm. You attempt to throw the end of the rope to the otherside
    hoping it will safely hook onto something on the other end. 
    You rope isn't long enough and you realize this wasn't probably a
    very good idea anyways. Now what?""", state


@choose_item.option('Use you axe', condition=lambda s: s.axe == True)
@default_template
def use_axe(state, *opts):
    return """You hold your axe in your hand and. "If only there was a way
    to chop myself to the otherside", you think.""", state


@choose_item.option('Use you torch', condition=lambda s: s.torch == True)
@default_template
def use_torch(state, *opts):
    return """You wave your torch over the chasm hoping to see the bottom. It cast shadows
    which bounce down the endless walls but never reveal the floor""", state


@choose_item.option('Examine the boulder')
@use_rope.option('Examine the boulder')
@use_axe.option('Examine the boulder')
@use_torch.option('Examine the boulder')
@default_template
def examine_boulder(state, *opts):
    return Div(
        P(
            """You examine the boulder. It looks like a map. The writing
            is worn but you think you can make it out."""
        ),
        Div(Pre(
            """To cross the crack, to make it back
to where
            
            """
        ))
    ), state




# default/custom template
# template reuse


if __name__ == '__main__':
    app.render()
