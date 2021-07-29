from typing import List
from string import Template

from grimoire.utils import make_decorator

from hype import (
    Doc,
    Html,
    Head,
    Style,
    A,
    Title,
    Body,
    Div,
    Ul,
    Li
)


def link(text, option_hash):
    return A(text, href=f"{option_hash}.html")


def default_page(
    title: str,
    bg_color: str = "#efefef",
    font_color: str = "#121212",
    link_color: str = "#6666bb"
):
    @make_decorator
    def inner(fn, state: str, *opts: List[int]):
        content, options, state = fn(state, *opts)
        return (
            Doc(
                Html(
                    Head(
                        Style(
                            get_style(
                                bg_color=bg_color,
                                font_color=font_color,
                                link_color=link_color
                            )
                        ),
                        Title(title)
                    ),
                    Body(
                        Div(
                            Div(_class="grid__left"),
                            Div(
                                content,
                                Ul(*[Li(link(o[0], o[1])) for o in options]),
                                _class="grid__content"
                            ),
                            Div(_class="grid__right"),
                            _class="grid",
                        ),
                    ),
                )
            ),
            state,
        )

    return inner


def get_style(**kwargs):
    tmplt = """
body {
    background-color: $bg_color;
    color: $font_color;
    font-size: 2rem;
    font-family: Georgia, 'Times New Roman', Times, serif; 
}

ul {
    list-style-type: none;
    padding-left: 0px;
}

a {
    color: $link_color;
    text-decoration: none;
}

.grid {
    display: grid;
    grid-template-areas: 'left content right';
    grid-template-columns: 1fr 1fr 1fr;
}


@media screen and (max-width: 1000px) {
    .grid {
        grid-template-columns: 0fr 1fr 0fr;
    }

    body {
        font-size: 3em;
    }

}
"""
    template = Template(tmplt)
    return template.substitute(kwargs)
