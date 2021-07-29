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
        opts_element.append(Span(link(previous[0], previous[1]), _class="previousious"))
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
                )
            ),
            state,
            previous,
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
    ), state, None, ("next", install)


@app.page()
@code_section(lexer=BashLexer)
def install(state, title, create_app):
    content = Div(
        H2("Install"),
        P("Install Grimoire via pip"),
    )
    code = "pip install grimoire-if"
    return content, code, state, ('previous', title), ('next', create_app)


@app.page()
@code_section(lexer=PythonLexer)
def create_app(state, install, create_page):
    content = Div(
        H2("Create an app"),
        P("Let's create an instance of a Grimoire app."),
    )
    code = """
from grimoire import Grimoire


app = Grimoire()
    """
    return content, code, state, ('previous', install), ('next', create_page)


@app.page()
@code_section(lexer=PythonLexer)
def create_page(state, create_app, render_app):
    content = Div(
        H2("Create your first page"),
        P("""Pages are simply functions decorated by a Grimoire app's .page method.
For your first page, pass the start keyword start=True"""),
        P("""Notice how the first, and only, argument of our page function is start. We'll get more into that 
later but it's important to always include it as the first argument. Every page function also must return 
some content to render and a state object."""),
    )
    code = """

@app.page(start=True)
def start(state):
    return "Hello, Grimoire!", state
    """
    return content, code, state, ('previous', create_app), ('next', render_app)


@app.page()
@code_section(lexer=PythonLexer)
def render_app(state, create_page, use_hype):
    content = Div(
        H2("Render the App"),
        P("""You are ready to render the app. Of course, there isn't much to our story yet.
Rendering should create a site/ directory with an index.html file associated with our
first page. Go ahead and load it into your browser."""),
        P("As we go through each step, render the app and explore the chages we've made.")
    )
    code = """
app.render()
    """
    return content, code, state, ('previous', create_page), ('next', use_hype)


@app.page()
@code_section(lexer=PythonLexer)
def use_hype(state, render_app, add_option):
    content = Div(
        H2("Use Hype"),
        P("""The content your page function returns is rendered using Python's built-in str method. So you
can include html directly in a string if you'd like."""),
        P(f"""Alternativley, Grimoire comes with a small library for creating html called 
{A("hype", href="https://github.com/scrussell24/hype-html", _class="content-link")}.
Import hype's classes and create html using only Python!"""),
    )
    code = """
from hype import *

@app.page(start=True)
def start(state):
    return Div(
        H1("Title"),
        "<p>Hello, <p>",
        P("Grimoire!")
    ), state
    """
    return content, code, state, ('previous', render_app), ('next', add_option)


@app.page()
@code_section(lexer=PythonLexer)
def add_option(state, use_hype, manage_state):
    content = Div(
        H2("Add Options"),
        P("""To add an option, create another page function (we don't need start=True this time). Add an argument to any
page that with to link to the new page with the same name as the page function. Use Girmoire's builtin link function to create
a link to the page."""),
        P("""You can add as many options as you like by continuing to add arguments.""")
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
    return content, code, state, ('previous', use_hype), ('next', manage_state)


@app.page()
@code_section(lexer=PythonLexer)
def manage_state(state, add_option, state_class):
    content = Div(
        H2("Manage State"),
        P("""The state object passed to your page function can be read and 
updated to manage the state of your application. By default it's a dictionary."""),
        P("Notice how the we access the message from the first page in the second page.")
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
    return content, code, state, ('previous', add_option), ('next', state_class)


@app.page()
@code_section(lexer=PythonLexer)
def state_class(state, manage_state, back):
    content = Div(
        H2("Custom State Class"),
        P("""Dictionaries are cool but not always the best way to structure our state.
You can add a custom state class when creating your app.""")
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
    return content, code, state, ('previous', manage_state), ('next', back)


@app.page()
@code_section(lexer=PythonLexer)
def back(state, state_class, default_template):
    content = Div(
        H2("Back to the beginning"),
        P("""Circular references are easy in Grimoire. Just add the option argument for an eariler page.""")
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
    return content, code, state, ('previous', state_class), ('next', default_template)


@app.page()
@code_section(lexer=PythonLexer)
def default_template(state, back, next_steps):
    content = Div(
        H2("Default Page"),
        P("""Grimoire comes packaged with a function to style your page
and render your options by default. It returns a decorator which can be
applied to your page functions.""")
    )
    code = """
from grimoire.templates import default_page


page = default_page("Minimal Example")


@app.page(start=True)
@page
def start(state, second):
    state.message = "Hello, traveller"
    return Div(
        P("Hello, Grimoire!")
    ), [("Go to the second page", second)], state


@app.page()
@page
def second(state, start):
    return Div(
        P(f"message: {state.message}")
    ), [("Start over", start)], state
    """
    return content, code, state, ('previous', back), ('next', next_steps)


@app.page()
@base
def next_steps(state, default_template, title):
    return Div(
        Div(_class="header"),
        P("""That's it! You've completed the Grimoire tutoiral. Check out the
the expamples directory in this repo for more."""),
        _class="title_page"
    ), state, ("previous", default_template), ('start over', title)


CSS = """body {
    background-color: #fefefe;
    color: #3d3d3d;
    font-size: 1.2rem;
    font-family: Georgia, 'Times New Roman', Times, serif;
    padding: 0px;
    margin: 0px;
}

h2 {
  color: #c8c8c8;  
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
    height: 75vh;   
}

.title_page {
    padding: 25px;
    height: 75vh;
}

.content_grid__left {
    padding: 25px;
    background-color: #3d3d3d;
    color: #fefefe;
}

.content-link {
    color: #bbbbff;
    text-decoration: none;
}

.content_grid__right {
    padding: 25px;
    background-color: #f8f8f8;
}

.header {
    height: 5vh; 
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
        height: 95vh;   
    }

    .title_page {
        height: 90vh;
    }

    .header {
        height: 0vh; 
    }


    body {
        font-size: 2.5em;
    }
}"""


if __name__ == "__main__":
    app.render("docs/")
