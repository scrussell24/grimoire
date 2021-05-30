from grimoire import Grimoire

from hype import *


def template(state, option_links):
        return Doc(
            Html(
                Body(
                    P(state['text']),
                    Ul(*[Li(A(o.option_text, href=f'{l}.html')) for l, o in option_links])
                )
            )     
        )


grim = Grimoire(template)

@grim.start_page
def start_page(state):
    state['day'] = 0
    state['sticks'] = 0
    state['text'] = f'you have arrived on a desolate planet. Day {state["day"]}. Stick {state["sticks"]}.'
    return state


@grim.option(start_page, "go north")
def north(state):
    state['day'] += 1
    state['text'] = f'You have travelled north, it took you one day. Day {state["day"]}. Stick {state["sticks"]}.'
    return state


@grim.option(start_page, "go south")
def south(state):
    state['day'] += 1
    state['text'] = f'You have travelled south, it took you one day. Day {state["day"]}. Stick {state["sticks"]}.'
    return state


@grim.option(start_page, "go east")
def east(state):
    state['day'] += 1
    state['text'] = f'You have travelled east, it took you one day. Day {state["day"]}. Stick {state["sticks"]}.'
    return state


@grim.option(start_page, "go west")
def west(state):
    if state['day'] < 10:
        state['day'] += 1
    state['text'] = f'You have travelled west, it took you one day. Day {state["day"]}. Stick {state["sticks"]}.'
    return state


@grim.redirect(west)
@grim.option(west, 'pick up a stick', lambda s: s['sticks'] < 10)
def pick_up_stick(state):
    state['sticks'] += 1
    return state

grim.option(north, 'start over (n)')(start_page)
grim.option(south, 'start over (s)')(start_page)
grim.option(east, 'start over (e)')(start_page)
grim.option(west, 'start over (w)')(start_page)


if __name__ == '__main__':
    grim.render()
