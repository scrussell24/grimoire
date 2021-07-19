# Grimoire

Grimoire is a Python library to create interactive fiction.
What makes Grimoire unique is that it pre-renders all possible
choices and simply outputs linked HTML files.

## Installation

```
pip install grimoire-if
```

## Usage

Check out some [examples](examples/).

### Your story begins

Begin by instantiating a Grimoire app.

```
from grimoire import Grimoire


app = Grimoire()
```

Then create our stories initial page.

```
@app.page(start=True)
def start(state):
    state['name'] = 'Grimoire'
    return f"Hello, Grimoire!", state
```

You can render our (rather boring) story right now by calling the app's render method.

```
app.render()
```

Grimoire added all the html files (in this case only the index.html file) into the site/ directory.

You can optionally pass a state class when creating your app.

```
@datalass
class State:
    name: Optional[str] = None


app = Grimoire(state=State)

@app.page(start=True)
def start(state):
    state.name = 'Grimoire'
    return f"Hello, {state.name}!", state
```

Grimoire uses [hype](https://github.com/scrussell24/hype-html) to render html and you can use it in your render functions.

```
from hype import *


@app.page(start=True)
def start(state):
    state.name = 'Grimoire'
    return H1(f"Hello, {state.name}!"), state
```

### Choose your own destiny

Let's add some options. We'll start by creating another page.

```
@app.page()
def next(state):
    return P("We're really moving now!"), state
```

Now go back to our first page and another argument, next. We'll import a helper function
called link from grimoire.tempaltes to construct the link using the option argument.

```
from grimoire.templates import link


@app.page(start=True)
def start(state, next):
    state.name = 'Grimoire'
    return Div(
        H1(f"Hello, {state.name}!"),
        link('Next Page', next)
    ), state
```
