import os
from copy import copy


os.environ['PYTHONHASHSEED'] = "0"


class Page:

    def __init__(self, fn, option_text, condition, template):
        self.fn = fn
        self.cache = []
        self.options = []
        self.redirect = None
        self.template = template
        self.condition = condition
        self.option_text = option_text

    def render(self, state, start=True):
        if not self.condition(state):
            return None
        
        if start:
            for root, _, files in os.walk("build"):
                for file in files:
                    os.remove(os.path.join(root, file))

        hashbrown = f'{hash(hash(self) + hash(str(state)))}'
        options = []
        text= ''
        if hashbrown not in self.cache:
            self.cache.append(hashbrown)
            text, state = self.fn(copy(state))
            if self.redirect:
                rrend = self.redirect.render(state, start=False)
                options = rrend[1] if rrend else []
                text = rrend[2] if rrend else ''
                html = self.redirect.template(text, state, options)
            else:
                for option in self.options:
                    rend = option.render(state, start=False)
                    if rend:
                        options.append((rend[0], option))
                html = self.template(text, state, options)
            filename =  'index.html' if start else f'{hashbrown}.html'
            with open(f'build/{filename}', 'w') as f:
                f.write(str(html))
        return hashbrown, options, text


class Grimoire:

    def __init__(self, template, state_class=None):
        self.template = template
        self.pages = {}
        self.start = None
        self.state_class = state_class

    def start_page(self, f):
        page = Page(f, None, lambda s: True, self.template)
        self.start = page
        self.pages[f] = page
        return f

    def option(self, parent, text, condition=lambda s: True):
        def decorator(f):
            page = Page(f, text, condition, self.template)
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
