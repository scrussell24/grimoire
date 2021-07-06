from typing import *
from functools import wraps
from dataclasses import dataclass

from grimoire import Grimoire

from hype import *
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, BashLexer


@dataclass
class State:
    test: Optional[str] = None


def make_decorator(f):
    '''A simple decorator for creating more decorators'''
    @wraps(f)
    def outter(g):
        @wraps(g)
        def inner(*args, **kwds):
            return f(g, *args, **kwds)
        return inner
    return outter


@make_decorator
def base(fn, state: State, *opts: List[Option]) -> Tuple[Element, State]:
    content, state = fn(state, *opts)
    previous =  opts[0] if len(opts) > 0 else None
    next = opts[1] if len(opts) > 1 else None
    opts = Div(_class="options")
    if previous:
        opts.append(Span(A(previous.text, href=f'{previous.hash}.html', _class="previous")))
    if next:
        opts.append(Span(A(next.text, href=f'{next.hash}.html', _class="next")))
    return Doc(
      Html(
        Head(
            Style(CSS),
            Style(HtmlFormatter().get_style_defs('.highlight'))
        ),
        Body(
          Div(
              Div(_class="grid__left"),
              Div(
                  content,
                  opts,
                  _class="grid__content"),
              Div(_class="grid__right"),
              _class="grid")
          )
      )     
    ), state


def code_section(lexer=PythonLexer):
    @make_decorator
    def inner(fn, state: State, *opts: List[Option]) -> Tuple[Element, State]:
        content, code, state = fn(state, *opts)
        return Div(
            Div(content, _class="content_grid__left"),
            Div(highlight(code, lexer(), HtmlFormatter()), _class="content_grid__right"),
            _class="content_grid"
        ), state
    return inner


app = Grimoire(state=State)


@app.start_page
@base
def start(state: State, *opts: List[Option]) -> Tuple[str, State]:
    return H1("Grimoire"), state


@app.option(start, "Installation")
@base
@code_section(lexer=BashLexer)
def install(state: State, *opts: List[Option]) -> Tuple[str, str, State]:
    content = Div(
        H2('Installation'),
        P('Install Grimoire via pip'),
        P('(Or just copy/paste the source, it\'s only about 100 lines of Python in a single file)')
    )
    code = 'pip install grimoire-if'
    return content, code, state


app.option(install, "Previous - Getting Started")(start)


@app.option(install, "Next - Create an app")
@base
@code_section()
def create_an_app(state: State, *opts: List[Option]) -> Tuple[str, str, State]:
    content = Div(
        H2('Create an app'),
        P('Instantiate an instance of a Grimoire app')
    )
    code = '''app = Grimoire()'''
    return content, code, state


app.option(create_an_app, "Previous - Installation")(install)


@app.option(create_an_app, "Next - Add your first page")
@base
@code_section()
def first_page(state: State, *opts: List[Option]) -> Tuple[str, str, State]:
    content = Div(
        H2('Add your first page'),
        P('Use the start_page decorator to decorate your render function')
    )
    code = '''@app.start_page
def start(state):
    state['name'] = 'Grimoire'
    return f"Hello, {state['name']}", state'''
    return content, code, state


CSS = '''body {
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
    grid-template-areas: 'left right';
    grid-template-columns: 1fr 1fr;
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

    body {
        font-size: 1.6em;
    }
}'''


if __name__ == '__main__':
    app.render(path="tutorial/")
