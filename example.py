from hype import *

from grimoire import Page


if __name__ == '__main__':

    # define pages
    first = Page(
        text='Choose your own adventure!'
    )

    class Second(Page):
        text = 'You chose {choice}!'

    
    rafting = Second(choice='Whitewater rafting')
    climbing = Second(choice='Climb Mount Everest')
    moon = Second(choice='Take a rocket to the moon')

    
    third = Page(
        text='You still need to do {choice}'
    )


    # hook'em up
    first.option('Go Whitewater rafting', rafting)
    first.option('Climb Mount Everest', climbing)
    first.option('To the moon', moon)
    rafting.option('what to do next?', third)
    climbing.option('what to do next?', third)
    moon.option('what to do next?', third)
    third.option('home', first)


    ## render
    first.render()
