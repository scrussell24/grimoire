import os
from copy import copy
from typing import List
from dataclasses import dataclass


from hype import *


os.environ['PYTHONHASHSEED'] = "0"


def DEFAULT_TEMPLATE(text: str, state, options: List[Option]):
    return Doc(
      Html(
        Body(
          P(text),
          Ul(*[Li(A(o.text, href=f'{o.hash}.html')) for o in options])
        )
      )     
    )


class Page:

    def __init__(self, fn, option_text, condition, template):
        self.fn = fn
        self.cache = []
        self.options = []
        self.redirect = None
        self.condition = condition
        self.option_text = option_text
        self.template = template if template else DEFAULT_TEMPLATE

    def render(self, state, start=True):
        # if the condition is not met, do not render this
        # page (also don't pass the link info back)
        if not self.condition(state):
            return None
        # clear out the site dir
        if start:
            for root, _, files in os.walk("site"):
                for file in files:
                    os.remove(os.path.join(root, file))

        page_hash = f'{hash(hash(self) + hash(str(state)))}'
        options = []
        text= ''
        if page_hash not in self.cache:
            self.cache.append(page_hash)
            text, state = self.fn(copy(state))
            if self.redirect:
                render = self.redirect.render(state, start=False)
                options = render[1] if render else []
                text = render[2] if render else ''
                html = self.redirect.template(text, state, options)
            else:
                for page in self.options:
                    render = page.render(state, start=False)
                    if render:
                        options.append(Option(render[0], page.option_text))
                html = self.template(text, state, options)
            filename =  'index.html' if start else f'{page_hash}.html'
            # write the file to the build dir
            with open(f'site/{filename}', 'w') as f:
                f.write(str(html))
        return page_hash, options, text


class Grimoire:

    def __init__(self, template=None, state=None):
        self.template = template
        self.pages = {}
        self.start = None
        self.state_class = state

    def start_page(self, f, template=None):
        template = template if template else self.template
        page = Page(f, None, lambda s: True, self.template)
        self.start = page
        self.pages[f] = page
        return f

    def option(self, parent, text, condition=lambda s: True, template=None):
        template = template if template else self.template
        def decorator(f):
            page = Page(f, text, condition, template)
            if f in self.pages:
                page.options = self.pages[f].options  
            self.pages[parent].options.append(page)
            self.pages[f] = page
            return f
        return decorator

    def redirect(self, parent):
        def decorator(f):
            self.pages[f].redirect = self.pages[parent]
            return f
        return decorator
    
    def render(self, **state):
        state = self.state_class(**state) if self.state_class else state
        self.start.render(state)


@dataclass
class Option:
    hash: str
    text: str
