from hype import *

from grimoire import Page


if __name__ == '__main__':

    third = Page(
        text='You still need to do {choice}',
        option_text='what do do next'
    )

    class Second(Page):
        text = 'You chose {choice}!'
        options = (third,)

    rafting = Second(
        option_text='Go Whitewater rafting',
        choice='Whitewater rafting'
    )

    climbing = Second(
        option_text='Climb Mount Everest',
        choice='Climb mount Everest'
    )

    rocket = Second(
        option_text='Go to the moon',
        choice='Take a rocket to the moon'
    )

    first = Page(
        text='Choose your own adventure!',
        options=(rafting, climbing, rocket),
        option_text="home"
    )

    third.options = (first,)

    first.render()

    
