from dataclasses import dataclass
from typing import Optional

from hype import (
    H1,
    H2,
    A,
    Body,
    Br,
    Div,
    Doc,
    Footer,
    Head,
    Html,
    I,
    Li,
    Link,
    Main,
    Meta,
    P,
    Section,
    Span,
    Style,
    Title,
    Ul,
)
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import BashLexer, PythonLexer

from grimoire import Grimoire
from grimoire.templates import link
from grimoire.utils import make_decorator


@dataclass
class State:
    test: Optional[str] = None


@make_decorator
def base(fn, state, *opts):
    content, state, previous, next = fn(state, *opts)
    opts_element = Div(_class="options")
    if previous:
        opts_element.append(Span(link(previous[0], previous[1])))
    if next:
        opts_element.append(Span(link(next[0], next[1]), style="float: right;"))
    return (
        Doc(
            Html(
                Head(
                    Title("Grimoire Tutorial: Getting Started"),
                    Meta(charset="utf-8"),
                    Meta(
                        name="viewport",
                        content="width=device-width, initial-scale=1",
                    ),
                    Link(
                        rel="stylesheet",
                        href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css",
                    ),
                    style,
                ),
                Body(
                    Main(content, _class="container"),
                    Footer(opts_element, _class="container"),
                    style="margin-top:5%;",
                ),
                lang="en",
                data_theme="light",
            )
        ),
        state,
    )


def code_section(lexer=PythonLexer):
    @make_decorator
    @base
    def inner(fn, state, *opts):
        header, paragraphs, code, state, previous, next = fn(state, *opts)
        return (
            Div(
                Section(
                    Div(H2(header), *[P(p) for p in paragraphs]),
                    _style="min-height: 25vh;",
                ),
                Section(
                    highlight(code, lexer(), HtmlFormatter()),
                    _style="min-height: 40vh; background-color: #edf0f3; padding: 20px;",
                ),
                _class="grid",
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
            H1("Welcome to the Grimoire Tutorial!"),
            P(
                """Grimoire is a Python library for creating interactive fiction as hyperlinked html."""
            ),
            P(
                f"""The source code is available on {A("github", href="https://github.com/scrussell24/grimoire")}
including the source for this {A("tutorial", href="https://github.com/scrussell24/grimoire/blob/main/examples/tutorial.py")}
which was created using Grimoire itself."""
            ),
        ),
        state,
        ("Get started", install),
        None,
    )


@app.page()
@code_section(lexer=BashLexer)
def install(state, title, create_app):
    return (
        "Installation",
        ["Install Grimoire via pip"],
        "pip install grimoire-if",
        state,
        ("previous", title),
        ("next", create_app),
    )


@app.page()
@code_section(lexer=PythonLexer)
def create_app(state, install, create_page):
    return (
        "Create an app",
        ["Create an instance of a Grimoire app."],
        """
from grimoire import Grimoire


app = Grimoire()
""",
        state,
        ("previous", install),
        ("next", create_page),
    )


@app.page()
@code_section(lexer=PythonLexer)
def create_page(state, create_app, render_app):
    return (
        "Create your first page",
        [
            f"""Pages are functions decorated by a Grimoire app's {I("page")} method.
For the first page, pass the start keyword argument {I("start=True")}. This will prompt grimoire to
name the associated html page index.html."""
            f"""Notice how the first, and only, argument of our page function is {I("state")}. We'll get more into that 
later, but it's important to always include it as the first argument. Every page function also must return 
some content to render and a state object."""
        ],
        """
@app.page(start=True)
def start(state):
    return "This is my first grimoire app.", state
""",
        state,
        ("previous", create_app),
        ("next", render_app),
    )


@app.page()
@code_section(lexer=PythonLexer)
def render_app(state, create_page, use_hype):
    return (
        "Render the App",
        [
            """You are ready to render the app. Rendering should create a site/ directory with 
an index.html file associated with our first page. Go ahead and load it into your browser.""",
            "As we go through each step, render the app and explore the chages we've made.",
        ],
        """
app.render()

# optionally pass an alternate path

app.render("docs/")
""",
        state,
        ("previous", create_page),
        ("next", use_hype),
    )


@app.page()
@code_section(lexer=PythonLexer)
def use_hype(state, render_app, add_option):
    return (
        "Use Hype",
        [
            f"""The content your page function returns is rendered using Python's 
built-in {A("str", href="https://docs.python.org/3/library/functions.html#func-str", _class="content-link")} 
function. So you can include html directly in a string if you'd like.""",
            f"""Alternativley, Grimoire comes with a small library for creating html called 
{A("hype", href="https://github.com/scrussell24/hype-html", _class="content-link")}.
Import hype's classes and create html using only Python!""",
        ],
        """
from hype import H1, P


@app.page(start=True)
def start(state):
    return Div(
        H1("My First Grimoire Story"),
        "<p>Inline html as a string<p>",
        P("Html using the Hype library")
    ), state
""",
        state,
        ("previous", render_app),
        ("next", add_option),
    )


@app.page()
@code_section(lexer=PythonLexer)
def add_option(state, use_hype, manage_state):
    return (
        "Add Options",
        [
            """Create another page function (we don't need start=True this time). To add this as an 
option to an existing page, pass an argument to the parent page which has the same name as the new page function. 
Use Grimoire's builtin link function to create a link to the page.""",
            """You can add as many options as you like by continuing to add arguments to a page function's
signature.""",
        ],
        """
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
""",
        state,
        ("previous", use_hype),
        ("next", manage_state),
    )


@app.page()
@code_section(lexer=PythonLexer)
def manage_state(state, add_option, state_class):
    return (
        "Manage State",
        [
            """The state object passed to your page function can be read and 
updated to manage the state of your application. By default it's a dictionary.""",
            "Notice how the we access the message from the first page in the second page.",
        ],
        """
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
""",
        state,
        ("previous", add_option),
        ("next", state_class),
    )


@app.page()
@code_section(lexer=PythonLexer)
def state_class(state, manage_state, back):
    return (
        "Custom State Class",
        [
            """Dictionaries are cool, but often a custom class will make writing our code much more enjoyable.
You can add a custom state class when creating your app."""
        ],
        """
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
""",
        state,
        ("previous", manage_state),
        ("next", back),
    )


@app.page()
@code_section(lexer=PythonLexer)
def back(state, state_class, default_template):
    return (
        "Back to the beginning",
        [
            """Circular references are easy in Grimoire. Just add the option argument for an eariler page.""",
            """Warning: Be careful about creating infinite loops. Grimoire will
continue rendering pages as long as it's seeing a version of the state that hasn't previously been rendered.""",
        ],
        """
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
""",
        state,
        ("previous", state_class),
        ("next", default_template),
    )


@app.page()
@code_section(lexer=PythonLexer)
def default_template(state, back, next_steps):
    return (
        "Default Page",
        [
            """Grimoire comes packaged with a function to style your page
and render your options by default. It returns a decorator which can be
applied to your page functions."""
        ],
        """
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
""",
        state,
        ("previous", back),
        ("next", next_steps),
    )


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


style = Style(
    """

.options {
    border-top: 1px solid #333333;
    padding-bottom: 40px;
    background-color: #ffffff;
}

footer {
    position: fixed; 
    bottom: 0;
    left: 0;
    right: 0;
    height: 50px;
}

/* generated by pygments */
pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.highlight .hll { background-color: #ffffcc }
.highlight { background: #f8f8f8; }
.highlight .c { color: #408080; font-style: italic } /* Comment */
.highlight .err { border: 1px solid #FF0000 } /* Error */
.highlight .k { color: #008000; font-weight: bold } /* Keyword */
.highlight .o { color: #666666 } /* Operator */
.highlight .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.highlight .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.highlight .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight .gd { color: #A00000 } /* Generic.Deleted */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gr { color: #FF0000 } /* Generic.Error */
.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: #00A000 } /* Generic.Inserted */
.highlight .go { color: #888888 } /* Generic.Output */
.highlight .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: #0044DD } /* Generic.Traceback */
.highlight .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #008000 } /* Keyword.Pseudo */
.highlight .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #B00040 } /* Keyword.Type */
.highlight .m { color: #666666 } /* Literal.Number */
.highlight .s { color: #BA2121 } /* Literal.String */
.highlight .na { color: #7D9029 } /* Name.Attribute */
.highlight .nb { color: #008000 } /* Name.Builtin */
.highlight .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight .no { color: #880000 } /* Name.Constant */
.highlight .nd { color: #AA22FF } /* Name.Decorator */
.highlight .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #0000FF } /* Name.Function */
.highlight .nl { color: #A0A000 } /* Name.Label */
.highlight .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight .nv { color: #19177C } /* Name.Variable */
.highlight .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mb { color: #666666 } /* Literal.Number.Bin */
.highlight .mf { color: #666666 } /* Literal.Number.Float */
.highlight .mh { color: #666666 } /* Literal.Number.Hex */
.highlight .mi { color: #666666 } /* Literal.Number.Integer */
.highlight .mo { color: #666666 } /* Literal.Number.Oct */
.highlight .sa { color: #BA2121 } /* Literal.String.Affix */
.highlight .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight .sc { color: #BA2121 } /* Literal.String.Char */
.highlight .dl { color: #BA2121 } /* Literal.String.Delimiter */
.highlight .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight .sx { color: #008000 } /* Literal.String.Other */
.highlight .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight .ss { color: #19177C } /* Literal.String.Symbol */
.highlight .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight .fm { color: #0000FF } /* Name.Function.Magic */
.highlight .vc { color: #19177C } /* Name.Variable.Class */
.highlight .vg { color: #19177C } /* Name.Variable.Global */
.highlight .vi { color: #19177C } /* Name.Variable.Instance */
.highlight .vm { color: #19177C } /* Name.Variable.Magic */
.highlight .il { color: #666666 } /* Literal.Number.Integer.Long */

"""
)


if __name__ == "__main__":
    app.render("docs/")
