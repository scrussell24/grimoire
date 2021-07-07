from grimoire import Grimoire, default_template, link


app = Grimoire()

# first page
@app.page(start=True)
@default_template
def start(state, *opts):
    state = {}
    return 'Hello Adventurer. Welcome to the world of Grimoire.', state


@start.option("test")
@default_template
def test(state, red, blue, green):
    return f'Choose a color: {link(green, "green")}, {link(red, "red")}, {link(blue, "blue")}', state


def choose_green(state):
    state['color'] = 'green'
    return state


def choose_blue(state):
    state['color'] = 'blue'
    return state


def choose_red(state):
    state['color'] = 'red'
    return state


@test.option('choose green', update=choose_green)
@test.option('choose blue',  update=choose_blue)
@test.option('choose red',  update=choose_red)
@default_template
def chose_color(state, *opts):
    return f'You chose {state["color"]}', state


chose_color.option('Start Over')(start)


# State class
# default/custom template
# link
# type hints
# template reuse


if __name__ == '__main__':
    app.render()
