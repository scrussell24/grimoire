from typing import List

from grimoire.utils import make_decorator

from hype import Doc, Html, Head, Title, Body, Div, Ul, Li, A


def link(text, option_hash):
    return A(text, href=f"{option_hash}.html")


def default_page(title: str):
    @make_decorator
    def inner(fn, state: str, *opts: List[int]):
        content, options, state = fn(state, *opts)
        return (
            Doc(
                Html(
                    Head(Title(title)),
                    Body(Div(content), Ul(*[Li(link(o[0], o[1])) for o in options])),
                )
            ),
            state,
        )

    return inner
