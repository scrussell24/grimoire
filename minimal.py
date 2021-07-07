from grimoire import Grimoire, default_template, link


app = Grimoire()


@app.page(start=True)
@default_template
def start(state, *opts):
    state = {}
    return 'You ', state


@start.option("test")
@default_template
def test(state, red, blue, green):
    return f'Choose a color: {link(green, "green")}, {link(red, "red")}, {link(blue, "blue")}', state


def update_color(color):
    def updater(state):
        state['color'] = color
        return state
    return updater


@test.option('choose green', update=update_color('green'))
@test.option('choose blue',  update=update_color('blue'))
@test.option('choose red',  update=update_color('red'))
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
