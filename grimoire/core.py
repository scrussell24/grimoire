import os
from copy import copy
from inspect import signature
from dataclasses import dataclass
from typing import List, Optional

from hype import *

from grimoire.utils import make_decorator


os.environ['PYTHONHASHSEED'] = "0"


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

    def __init__(self, fn, option_text, condition, update):
        self.fn = fn
        self.cache = []
        self.options = []
        self.redirect = None
        self.update = update
        self.condition = condition
        self.option_text = option_text

    def render(self, state, path, start=True):
        
        # clear out the site dir
        if start:
            for root, _, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))
        
        # if the condition is not met, do not render this
        # page (also don't pass the link info back)
        if not self.condition(state):
            return None

        # run update function
        state = self.update(state)

        page_hash = f'{hash(hash(self) + hash(str(state)))}'
        if page_hash not in self.cache:
            self.cache.append(page_hash)
            params = signature(self.fn).parameters
            _, new_state = self.fn(copy(state), *[Option('', '', '') for _ in range(len(params) - 1)])
            options = []
            for page in self.options:
                child_hash = page.render(copy(new_state), path, start=False)
                if child_hash:
                    options.append(Option(child_hash, page.option_text, page.fn.__name__))
            # filtered_options = []
            # for param in params:
            #     for opt in options:
            #         if param == 'opts' or param == opt.name:
            #             filtered_options.append(opt)
            content, state = self.fn(state, *options)
            filename =  'index.html' if start else f'{page_hash}.html'
            # write the file to the build dir
            with open(f'{path}{filename}', 'w') as f:
                f.write(str(content))
        return page_hash


class Grimoire:

    def __init__(self, state=None):
        self.pages = {}
        self.start = None
        self.state_class = state

    def begin(self, f):
        page = Page(f, '', lambda s: True, update=lambda s: s)
        self.start = page
        self.pages[f] = page
        setattr(f, 'option', self.option(f))
        return f

    def option(self, parent):
        def outter(text, condition=lambda s: True, update=lambda s: s):
            def decorator(f):
                page = Page(f, text, condition, update)
                if f in self.pages:
                    page.options = self.pages[f].options
                self.pages[parent].options.append(page)
                self.pages[f] = page
                setattr(f, 'option', self.option(f))
                return f
            return decorator
        return outter
    
    def render(self, path="site/"):
        state = self.state_class() if self.state_class else {}
        self.start.render(state, path)


@dataclass
class Option:
    hash: str
    text: str
    name: str
