from typing import Optional
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
    content, state, previous, next = fn(state, *opts)
    opts_element = Div(_class="options")
    if previous:
        opts_element.append(
            Span(link(previous[0], previous[1]), _class="previous option")
        )
    if next:
        opts_element.append(Span(link(next[0], next[1]), _class="next option"))
    return (
        Doc(
            Html(
                Head(
                    Title("Grimoire Tutorial: Getting Started"),
                    Meta(name="viewport"),
                    Meta(name="description", content="A tutorial of the Grimoire interactive fiction Python library."),
                    Link(rel="stylesheet", href="style.css"),
                ),
                Body(
                    Div(
                        Div(_class="grid__left"),
                        Div(content, opts_element, _class="grid__content"),
                        Div(_class="grid__right"),
                        _class="grid",
                    )
                ),
    
                lang="en",
            )
        ),
        state,
    )


def code_section(lexer=PythonLexer):
    @make_decorator
    @base
    def inner(fn, state, *opts):
        content, code, state, previous, next = fn(state, *opts)
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
                ),
            ),
            state,
            previous,
            next,
        )

    return inner


app = Grimoire(state=State)


@app.page(start=True)
@base
def title(state, install):
    return (
        Div(
            Div(_class="header"),
            H1("Welcome to the Grimoire Tutorial!"),
            P(
                """Grimoire is a Python library for creating interactive fiction as hyperlinked html."""
            ),
            P(
                f"""The source code is available on {A("github", href="https://github.com/scrussell24/grimoire")}
including the source for this {A("tutorial", href="https://github.com/scrussell24/grimoire/blob/main/examples/tutorial.py")}
which was created using Grimoire itself."""
            ),
            _class="title_page",
        ),
        state,
        ("Get started", install),
        None,
    )


@app.page()
@code_section(lexer=BashLexer)
def install(state, title, create_app):
    content = Div(
        H2("Installation"),
        P("Install Grimoire via pip"),
    )
    code = "pip install grimoire-if"
    return content, code, state, ("previous", title), ("next", create_app)


@app.page()
@code_section(lexer=PythonLexer)
def create_app(state, install, create_page):
    content = Div(
        H2("Create an app"),
        P("Create an instance of a Grimoire app."),
    )
    code = """
from grimoire import Grimoire


app = Grimoire()
    """
    return content, code, state, ("previous", install), ("next", create_page)


@app.page()
@code_section(lexer=PythonLexer)
def create_page(state, create_app, render_app):
    content = Div(
        H2("Create your first page"),
        P(
            f"""Pages are functions decorated by a Grimoire app's {I("page")} method.
For the first page, pass the start keyword argument {I("start=True")}. This will prompt grimoire to
name the associated html page index.html."""
        ),
        P(
            f"""Notice how the first, and only, argument of our page function is {I("state")}. We'll get more into that 
later, but it's important to always include it as the first argument. Every page function also must return 
some content to render and a state object."""
        ),
    )
    code = """

@app.page(start=True)
def start(state):
    return "This is my first grimoire app.", state
    """
    return content, code, state, ("previous", create_app), ("next", render_app)


@app.page()
@code_section(lexer=PythonLexer)
def render_app(state, create_page, use_hype):
    content = Div(
        H2("Render the App"),
        P(
            """You are ready to render the app. Rendering should create a site/ directory with 
an index.html file associated with our first page. Go ahead and load it into your browser."""
        ),
        P(
            "As we go through each step, render the app and explore the chages we've made."
        ),
    )
    code = """
app.render()

# optionally pass an alternate path

app.render("docs/")
    """
    return content, code, state, ("previous", create_page), ("next", use_hype)


@app.page()
@code_section(lexer=PythonLexer)
def use_hype(state, render_app, add_option):
    content = Div(
        H2("Use Hype"),
        P(
            f"""The content your page function returns is rendered using Python's 
built-in {A("str", href="https://docs.python.org/3/library/functions.html#func-str", _class="content-link")} 
function. So you can include html directly in a string if you'd like."""
        ),
        P(
            f"""Alternativley, Grimoire comes with a small library for creating html called 
{A("hype", href="https://github.com/scrussell24/hype-html", _class="content-link")}.
Import hype's classes and create html using only Python!"""
        ),
    )
    code = """
from hype import H1, P


@app.page(start=True)
def start(state):
    return Div(
        H1("My First Grimoire Story"),
        "<p>Inline html as a string<p>",
        P("Html using the Hype library")
    ), state
    """
    return content, code, state, ("previous", render_app), ("next", add_option)


@app.page()
@code_section(lexer=PythonLexer)
def add_option(state, use_hype, manage_state):
    content = Div(
        H2("Add Options"),
        P(
            """Create another page function (we don't need start=True this time). To add this as an 
option to an existing page, pass an argument to the parent page which has the same name as the new page function. 
Use Grimoire's builtin link function to create a link to the page."""
        ),
        P(
            """You can add as many options as you like by continuing to add arguments to a page function's
signature."""
        ),
    )
    code = """
from grimoire.templates import link


@app.page(start=True)
def start(state, second):
    return Div(
        P("Hello, Grimoire!"),
        Ul(Li(link("Go to the second page", second)))
    ), state


@app.page()
def second(state):
    return Div(
        P("I'm the second page.")
    ), state
    """
    return content, code, state, ("previous", use_hype), ("next", manage_state)


@app.page()
@code_section(lexer=PythonLexer)
def manage_state(state, add_option, state_class):
    content = Div(
        H2("Manage State"),
        P(
            """The state object passed to your page function can be read and 
updated to manage the state of your application. By default it's a dictionary."""
        ),
        P(
            "Notice how the we access the message from the first page in the second page."
        ),
    )
    code = """
@app.page(start=True)
def start(state, second):
    state["message"] = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!"),
        Ul(Li(link("Go to the second page", second)))
    ), state


@app.page()
def second(state):
    return Div(
        P(f"message: {state['message']}")
    ), state
    """
    return content, code, state, ("previous", add_option), ("next", state_class)


@app.page()
@code_section(lexer=PythonLexer)
def state_class(state, manage_state, back):
    content = Div(
        H2("Custom State Class"),
        P(
            """Dictionaries are cool, but often a custom class will make writing our code much more enjoyable.
You can add a custom state class when creating your app."""
        ),
    )
    code = """
from dataclasses import dataclass


@dataclass
class State:
    message: str = ""


app = Grimoire(State)


@app.page(start=True)
def start(state, second):
    state.message = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!"),
        Ul(Li(link("Go to the second page", second)))
    ), state


@app.page()
def second(state):
    return Div(
        P(f"message: {state.message}")
    ), state
    """
    return content, code, state, ("previous", manage_state), ("next", back)


@app.page()
@code_section(lexer=PythonLexer)
def back(state, state_class, default_template):
    content = Div(
        H2("Back to the beginning"),
        P(
            """Circular references are easy in Grimoire. Just add the option argument for an eariler page."""
        ),
        P(
            """Warning: Be careful about creating infinite loops. Grimoire will
continue rendering pages as long as it's seeing a version of the state that hasn't previously been rendered."""
        ),
    )
    code = """
@app.page(start=True)
def start(state, second):
    state.message = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!"),
        Ul(Li(link("Go to the second page", second)))
    ), state


@app.page()
def second(state, start):
    return Div(
        P(f"message: {state.message}"),
        Ul(Li(link("Start over", start)))
    ), state
    """
    return content, code, state, ("previous", state_class), ("next", default_template)


@app.page()
@code_section(lexer=PythonLexer)
def default_template(state, back, next_steps):
    content = Div(
        H2("Default Page"),
        P(
            """Grimoire comes packaged with a function to style your page
and render your options by default. It returns a decorator which can be
applied to your page functions."""
        ),
    )
    code = """
from grimoire.templates import default_page


@app.page(start=True)
@default_page("Minimal Example")
def start(state, second):
    state.message = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!")
    ), [("Go to the second page", second)], state

# Also try changing up some of the colors

@app.page()
default_page(
    "Minimal Example",
    primary_bg_color="#ff0000",
    secondary_bg_color="#00ff00"
    font_color="#bbbbbb"
)
def second(state, start):
    return Div(
        P(f"message: {state.message}")
    ), [("Start over", start)], state
    """
    return content, code, state, ("previous", back), ("next", next_steps)


@app.page()
@base
def next_steps(state, default_template, title):
    return (
        Div(
            Div(_class="header"),
            H1("You're Done!"),
            P(
                """That's it! You've completed the Grimoire tutoiral. As you can
see, there's not much to it. Grimiore is purposeley very minimal and our belief is
that many features can be easily implemented using plain old vanilla Python on top
of Grimoire."""
            ),
            P(
                f"""Check some further {A("examples", href="https://github.com/scrussell24/grimoire/tree/main/examples")}:"""
            ),
            Br(),
            Ul(
                Li(
                    A(
                        "A Desolate Planet",
                        href="https://scrussell24.github.io/grimoire/example/index.html",
                    )
                ),
                Li(
                    A(
                        "Rock, Paper, Scissors",
                        href="https://scrussell24.github.io/grimoire/rps/index.html",
                    )
                ),
            ),
            _class="title_page",
        ),
        state,
        ("previous", default_template),
        ("start over", title),
    )


if __name__ == "__main__":
    app.render("docs/")
