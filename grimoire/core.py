import os
from copy import copy
from inspect import signature
from dataclasses import dataclass
from typing import List, Optional



from hype import *


os.environ['PYTHONHASHSEED'] = "0"


def default_template(content: str, *opts: List[Option]):
    return Doc(
      Html(
        Body(
          Div(content),
          Ul(*[Li(Link(o)) for o in opts])
        )
      )     
    )


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
            for root, _, files in os.walk("site"):
                for file in files:
                    os.remove(os.path.join(root, file))

        page_hash = f'{hash(hash(self) + hash(str(state)))}'
        options = []
        content = ''
        if page_hash not in self.cache:
            self.cache.append(page_hash)
            params = signature(self.fn).parameters
            content, state = self.fn(copy(state), *[Option('', '') for n in range(len(params) - 1)])
            if self.redirect:
                render = self.redirect.render(state, path, start=False)
                options = render[1] if render else []
                content = render[2] if render else ''
            else:
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

    @staticmethod
    def Link(opt: Option, text: Optional[str] = None):
        text = text if text else opt.text
        return A(text, href=f'{opt.hash}.html')

    def __init__(self, state=None):
        self.pages = {}
        self.start = None
        self.state_class = state

    def start_page(self, f):
        page = Page(f, None, lambda s: True)
        self.start = page
        self.pages[f] = page
        return f

    def option(self, parent, text, condition=lambda s: True):
        def decorator(f):
            page = Page(f, text, condition)
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
    
    def render(self, path="site/", **state):
        state = self.state_class(**state) if self.state_class else state
        self.start.render(state, path)


@dataclass
class Option:
    hash: str
    text: str
