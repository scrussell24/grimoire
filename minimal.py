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
def test(state, green, blue, red):
    return f'Choose a color: {link(green, "green")}, {link(red, "red")}, {link(blue, "blue")}', state


@test.option('green')
def choose_green(state):
    state['color'] = 'green'
    return state


@test.option('blue')
def choose_blue(state):
    state['color'] = 'blue'
    return state


@test.option('red')
def choose_red(state):
    state['color'] = 'red'
    return state


@choose_green.redirect
@choose_blue.redirect
@choose_red.redirect
@default_template
def chose_color(state, *opts):
    return f'You chose {state["color"]}', state


chose_color.option('Start Over')(start)


# State class
# default/custom template
# link


if __name__ == '__main__':
    app.render()
