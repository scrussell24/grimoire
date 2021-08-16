from typing import List
from string import Template

from grimoire.utils import make_decorator

from hype import Doc, Html, Head, Style, A, Title, Body, Div, Ul, Li


def link(text, option_hash):
    return A(text, href=f"{option_hash}.html")


def default_page(
    title: str,
    primary_bg_color: str = "#efefef",
    secondary_bg_color: str = "#e4e4e4",
    font_color: str = "#121212",
    link_color: str = "#6666bb",
    font_family: str = "Garamond, 'Times New Roman', Times, serif",
    font_weight: str = "normal",
    line_height: str = "1em",
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
                                primary_bg_color=primary_bg_color,
                                secondary_bg_color=secondary_bg_color,
                                font_color=font_color,
                                link_color=link_color,
                                font_family=font_family,
                                font_weight=font_weight,
                                line_height=line_height,
                            )
                        ),
                        Title(title),
                    ),
                    Body(
                        Div(
                            Div(_class="grid__left"),
                            Div(
                                content,
                                Ul(*[Li(link(o[0], o[1])) for o in options]),
                                _class="grid__content",
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
    padding: 0px;
    margin: 0px;
    color: $font_color;
    font-size: 2rem;
    font-weight: $font_weight;
    font-family: $font_family;
    background-color: $primary_bg_color;
    line-height: $line_height;
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
    grid-template-columns: 1fr 2fr 1fr;
}

.grid__left, .grid__right {
    background-color: $secondary_bg_color;
    height: 100vh;
}


.grid__content {
    background-color: $primary_bg_color;
    height: 100vh;
    padding: 20px;
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
