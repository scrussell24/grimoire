import os


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
        if hashbrown not in self.cache:
            self.cache.append(hashbrown)
            state = self.fn(state.copy())
            if self.redirect:
                options = self.redirect.render(state, start=False)
                options = options[1] if options else []
                html = self.redirect.template(state, options)
            else:
                for option in self.options:
                    rend = option.render(state, start=False)
                    if rend:
                        options.append((rend[0], option))
                html = self.template(state, options)
            filename =  'index.html' if start else f'{hashbrown}.html'
            with open(f'build/{filename}', 'w') as f:
                f.write(str(html))
        return hashbrown, options


class Grimoire:

    def __init__(self, template):
        self.template = template
        self.pages = {}
        self.start = None

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
        self.start.render(state)
