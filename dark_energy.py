from functools import wraps
from dataclasses import dataclass, asdict

from hype import *

from grimoire import Page



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
    p1: str
    freq: int = None
    message: str = None
    p2: str = None
    p3: str = None


@make_decorator
def stateDeserializer(fn, page, state, option_links):
    return fn(page, State(**state), option_links)


class DePage(Page):

    @stateDeserializer
    def template(self, state, option_links):
        p1 = state.p1.format(**asdict(state))
        return Doc(
            Html(
                Meta(charset="utf-8"),
                Body(
                    P(p1),
                    Ul(*[Li(A(o.option_text, href=f'{l}.html')) for l, o in option_links])
                ),
                lang="en"
            )     
        )


# pages

dark_energy = DePage(
    p1='''
    Dark Energy

    by Scott Russell
    '''
)

def modulator(state):
    if state['freq'] == 0:
        state['message'] = mix_up(state['message'])
    return state

introduction = DePage(
    p1='{message}',
    message='Can you hear me?',
    freq=0,
    updater=modulator
)

no = DePage(
    p1='{message}',
    message='Let me try modulating the frequency',
    freq=1,
    updater=modulator
)

yes = DePage(
    p1='{message}',
    message='Good to hear',
    updater=modulator
)


dark_energy.option('start', introduction)
introduction.option('yes', yes)
introduction.option('no', no)


def mix_up(first):
    new_first = first[2:]
    new_second = first[:2]
    return " ".join((new_first, new_second))


if __name__ == '__main__':
    dark_energy.render()
