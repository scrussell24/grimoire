import os
from copy import copy
from functools import wraps
from inspect import signature
from dataclasses import dataclass
from typing import List, Optional

from hype import *


os.environ['PYTHONHASHSEED'] = "0"


def make_decorator(f):
    '''A simple decorator for creating more decorators'''
    @wraps(f)
    def outter(g):
        @wraps(g)
        def inner(*args, **kwds):
            return f(g, *args, **kwds)
        return inner
    return outter


def link(opt: Option, text: Optional[str] = None):
        text = text if text else opt.text
        return A(text, href=f'{opt.hash}.html')  


@make_decorator
def default_template(fn, state: str, *opts: List[Option]):
    content, state = fn(state, *opts)
    return Doc(
        Html(
            Body(
                Div(content),
                Ul(*[Li(link(o)) for o in opts])
            )
        )     
    ), state   


class Page:

    def __init__(self, fn, option_text, condition):
        self.fn = fn
        self.cache = []
        self.options = []
        self.redirect = None
        self.condition = condition
        self.option_text = option_text

    def render(self, state, path, start=True):
        # if the condition is not met, do not render this
        # page (also don't pass the link info back)
        if not self.condition(state):
            return None
        # clear out the site dir
        if start:
            for root, _, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))

        page_hash = f'{hash(hash(self) + hash(str(state)))}'
        options = []
        content = ''
        if page_hash not in self.cache:
            self.cache.append(page_hash)
            if self.redirect:
                state = self.fn(copy(state))
                if len(state) > 1:
                    # Just incase the user sends unused content back
                    # if there's a redirect we only care about state
                    # TODO maybe warning here?
                    state = state[1]
                render = self.redirect.render(state, path, start=False)
                options = render[1] if render else []
                content = render[2] if render else ''
            else:
                params = signature(self.fn).parameters
                content, state = self.fn(copy(state), *[Option('', '') for n in range(len(params) - 1)])
                for page in self.options:
                    render = page.render(state, path, start=False)
                    if render:
                        options.append(Option(render[0], page.option_text))
                content, state = self.fn(copy(state), *options)
            filename =  'index.html' if start else f'{page_hash}.html'
            # write the file to the build dir
            with open(f'{path}{filename}', 'w') as f:
                f.write(str(content))
        return page_hash, options, content  


class Grimoire:

    def __init__(self, state=None):
        self.pages = {}
        self.start = None
        self.state_class = state

    def page(self, start=False):
        def decorator(f):
            page = Page(f, '', lambda s: True)
            if start:
                self.start = page
            self.pages[f] = page
            setattr(f, 'option', self.option(f))
            setattr(f, 'redirect', self.redirect(f))
            return f
        return decorator

    def option(self, parent):
        def outter(text, condition=lambda s: True):
            def decorator(f):
                page = Page(f, text, condition)
                if f in self.pages:
                    page.options = self.pages[f].options  
                self.pages[parent].options.append(page)
                self.pages[f] = page
                setattr(f, 'option', self.option(f))
                setattr(f, 'redirect', self.redirect(f))
                return f
            return decorator
        return outter

    def redirect(self, parent):
        def decorator(f):
            if f not in self.pages:
                page = Page(f, '', lambda s: True)
                self.pages[f] = page
            if parent not in self.pages:
                page = Page(parent, '', lambda s: True)
                self.pages[parent] = page
            self.pages[parent].redirect = self.pages[f]
            setattr(f, 'option', self.option(f))
            setattr(f, 'redirect', self.redirect(f))
            return f
        return decorator
    
    def render(self, path="site/"):
        state = self.state_class() if self.state_class else {}
        self.start.render(state, path)


@dataclass
class Option:
    hash: str
    text: str
