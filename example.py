from grimoire import Grimoire

from hype import *


def template(text, option_links):
        return Doc(
            Html(
                Body(
                    P(text),
                    Ul(*[Li(A(o.option_text, href=f'{l}.html')) for l, o in option_links])
                )
            )     
        )


grim = Grimoire(template)

@grim.start_page
def start_page(state):
    state['day'] = 0
    return f'you have arrived on a desolate planet. Day {state["day"]}', state


@grim.option(start_page, "go north")
def north(state):
    state['day'] += 1
    return f'You have travelled north, it took you one day. Day {state["day"]}', state


@grim.option(start_page, "go south")
def south(state):
    state['day'] += 1
    return f'You have travelled south, it took you one day. Day {state["day"]}', state


@grim.option(start_page, "go east")
def east(state):
    state['day'] += 1
    return f'You have travelled east, it took you one day. Day {state["day"]}', state


@grim.option(start_page, "go west")
def west(state):
    state['day'] += 1
    return f'You have travelled west, it took you one day. Day {state["day"]}', state


grim.option(north, 'start over')(start_page)
grim.option(south, 'start over')(start_page)
grim.option(east, 'start over')(start_page)
grim.option(west, 'start over')(start_page)


if __name__ == '__main__':
    grim.render()
