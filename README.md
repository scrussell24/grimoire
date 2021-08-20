# Grimoire

Grimoire is a Python library for creating interactive fiction as hyperlinked html.

![tests](https://github.com/scrussell24/grimoire/actions/workflows/main.yml/badge.svg)

## Installation

```
pip install grimoire-if
```

## Usage

Check out the [tutorial](https://scrussell24.github.io/grimoire/)
created in Grimoire itself ([source](https://github.com/scrussell24/grimoire/blob/main/examples/tutorial.py)).

### Get started

Create an instance of a Grimoire app.

```
from grimoire import Grimoire


app = Grimoire()
```
### Add your first page

Create a function decorated by your app's page method. Pass the
keyword argument, start=True for the first page.

```
@app.page(start=True)
def start(state):
    return "This is my first grimoire app.", state
```
### Render your story

You can render our (rather boring) story right now by calling the app's render method.

```
# will create all the file in the /site directory

app.render()

# optionally pass an alternate path

app.render("docs/")
```

### Inline html

The content your page function returns is rendered using Python's 
built-in [str](https://docs.python.org/3/library/functions.html#func-str) function, so you can include html directly in a string if you'd like.

Alternativley, Grimoire comes with a small library for creating html called [hype](https://github.com/scrussell24/hype-html).
Import hype's classes and create html using only Python!

```
from hype import H1, P


@app.page(start=True)
def start(state):
    return Div(
        H1("My First Grimoire Story"),
        "<p>Inline html as a string<p>",
        P("Html using the Hype library")
    ), state
```

### Add an option to your first page

Create another page function (we don't need start=True this time). To add this as an option to an existing page, pass an argument to the parent page which has the same name as the new page function. 
Use Grimoire's builtin link function to create a link to the page.

You can add as many options as you like by continuing to add arguments to a parent page's function signature.

```
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
```

### Manage your stories state

The state object passed to your page function can be read and 
updated to manage the state of your application. By default it's a dictionary.

Notice how the we access the message from the first page in the second page.

```
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
```

### Use a custom state class

Dictionaries are cool, but often a custom class will make writing our code much more enjoyable. You can add a custom state class when creating your app.

```
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
```

### Back to the beginning

Circular references are easy in Grimoire. Just add the option argument for an eariler page.

Warning: Be careful about creating infinite loops. Grimoire will
continue rendering pages as long as it's seeing a version of the state that hasn't previously been rendered.

```
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
```

### Default page function

Grimoire comes packaged with a function to style your page
and render your options by default. It returns a decorator which can be
applied to your page functions.

```
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
```

### Next Steps

That's it! You've completed the Grimoire tutoiral. As you can
see, there's not much to it. Grimiore is purposeley very minimal and our belief is that many features can be easily implemented using plain old vanilla Python on top of Grimoire.

Check some further [examples](https://github.com/scrussell24/grimoire/tree/main/examples):

* [A Desolate Planet](https://scrussell24.github.io/grimoire/example/index.html)
* [Rock, Paper, Scissors](https://scrussell24.github.io/grimoire/rps/index.html)