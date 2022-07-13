from string import Template
from typing import Any, Callable, List, Tuple

from hype import (
    A,
    Body,
    Doc,
    Element,
    Head,
    Html,
    Li,
    Link,
    Main,
    Meta,
    Section,
    Style,
    Title,
    Ul,
)

from grimoire.errors import GrimoireInvalidOption
from grimoire.utils import make_decorator


def link(text: str, option_hash: str) -> Element:
    if callable(option_hash):
        raise GrimoireInvalidOption(option_hash)
    return A(text, href=f"{option_hash}.html")


def default_page(title: str) -> Callable:
    @make_decorator
    def inner(fn: Callable, state: str, *opts: List[str]) -> Tuple[Element, Any]:
        content, options, state = fn(state, *opts)
        return (
            Doc(
                Html(
                    Head(
                        Title("Grimoire Story"),
                        Meta(charset="utf-8"),
                        Meta(
                            name="viewport",
                            content="width=device-width, initial-scale=1",
                        ),
                        Link(
                            rel="stylesheet",
                            href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css",
                        ),
                        Style(
                            """
    ul {
        padding-left: 0px !important;
    }

    li {
        list-style: none !important;
    }"""
                        ),
                    ),
                    Body(
                        Main(
                            content,
                            Section(
                                Ul(*[Li(link(o[0], o[1])) for o in options]),
                            ),
                            _class="container",
                        ),
                    ),
                    lang="en",
                    data_theme="dark",
                )
            ),
            state,
        )

    return inner
