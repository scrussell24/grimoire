import os


os.environ['PYTHONHASHSEED'] = "0"


class Page:

    def __init__(self, fn, option_text, template):
        self.fn = fn
        self.cache = []
        self.options = []
        self.template = template
        self.option_text = option_text

    def render(self, state, start=True):
        if start:
            for root, _, files in os.walk("build"):
                for file in files:
                    os.remove(os.path.join(root, file))

        hashbrown = f'{hash(hash(self) + hash(str(state)))}'
        if hashbrown not in self.cache:
            self.cache.append(hashbrown)
            text, state = self.fn(state.copy())
            options = [(o.render(state, start=False), o) for o in self.options]
            html = self.template(text, options)
            filename =  'index.html' if start else f'{hashbrown}.html'
            with open(f'build/{filename}', 'w') as f:
                f.write(str(html))
        return hashbrown


class Grimoire:

    def __init__(self, template):
        self.template = template
        self.pages = {}
        self.start = None

    def start_page(self, f):
        page = Page(f, 'start over', self.template)
        self.start = page
        self.pages[f] = page
        return f

    def option(self, parent, text):
        def decorator(f):
            page = self.pages[f] if f in self.pages else Page(f, text, self.template)
            self.pages[parent].options.append(page)
            self.pages[f] = page
            return f
        return decorator
    
    def render(self, **state):
        self.start.render(state)
