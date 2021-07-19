from typing import *
from dataclasses import dataclass

from grimoire import Grimoire
from grimoire.templates import link
from grimoire.utils import make_decorator

from hype import *
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, BashLexer


@dataclass
class State:
    test: Optional[str] = None


@make_decorator
def base(fn, state, *opts):
    content, state, prev, next = fn(state, *opts)
    opts_element = Div(_class="options")
    if prev:
        opts_element.append(Span(link(prev[0], prev[1]), _class="previous"))
    if next:
        opts_element.append(Span(link(next[0], next[1]), _class="next"))
    return (
        Doc(
            Html(
                Head(
                    Style(CSS),
                    Style(HtmlFormatter().get_style_defs(".highlight"))
                ),
                Body(
                    Div(
                        Div(_class="grid__left"),
                        Div(content, opts_element, _class="grid__content"),
                        Div(_class="grid__right"),
                        _class="grid",
                    )
                ),
            )
        ),
        state
    )


def code_section(lexer=PythonLexer):
    @make_decorator
    @base
    def inner(fn, state, *opts):
        content, code, state, prev, next = fn(state, *opts)
        return (
            Div(
                Div(_class="header"),
                Div(
                    Div(content, _class="content_grid__left"),
                    Div(
                        highlight(code, lexer(), HtmlFormatter()),
                        _class="content_grid__right",
                    ),
                    _class="content_grid",
                )
            ),
            state,
            prev,
            next
        )
    return inner


app = Grimoire(state=State)


@app.page(start=True)
@base
def title(state, install):
    return Div(
        Div(_class="header"),
        H1("Grimoire"),
        P("A library for creating interactive fiction as linked hypertext."),
        _class="title_page"
    ), state, None, ("Get Started", install)


@app.page()
@code_section(lexer=BashLexer)
def install(state, title):
    content = Div(
        H2("Installation"),
        P("Install Grimoire via pip"),
        P("(Or just copy/paste the source, it's only about 100 lines of Python in a single file)"),
    )
    code = "pip install grimoire-if"
    return content, code, state, ('prev', title), ('next', '')


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
    color: #192f50;
    text-decoration: none;
}

.grid {
    display: grid;
    grid-template-areas: 'left content right';
    grid-template-columns: 1fr 3fr 1fr;
}

.content_grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto;
    grid-template-areas: 
        "header"
        "left right";
    height: 50vh;   
}

.title_page {
    height: 50vh;
}

.content_grid__left {
    padding: 20px;
    background-color: #333333;
    color: #fefefe;
}

.content_grid__right {
    padding: 25px;
    background-color: #f8f8f8;
}

.header {
    height: 15vh; 
}

.options {
    padding: 20px;
    height: 200px;
}

.next {
    float: right;
}

 @media screen and (max-width: 1000px) {
    .grid {
        grid-template-columns: 0fr 1fr 0fr;
    }

    .content_grid {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas: 
            "left"
            "right";
        height: 90vh;   
    }

    .title_page {
        height: 90vh;
    }

    .header {
        height: 0vh; 
    }


    body {
        font-size: 4em;
    }
}"""


if __name__ == "__main__":
    app.render()
