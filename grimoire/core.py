import os
from uuid import uuid4

from hype import *


os.environ['PYTHONHASHSEED'] = "0"


class Page:
    _cache = []

    def __init__(
        self,
        updater=None,
        **state
    ):
        self.state = state
        self.options = []
        self.updater = updater
        self.option_text = ""
        self.id = uuid4()
    
    def option(self, option_text, page):
        page.option_text = option_text
        self.options.append(page)
    
    def template(self, state, option_links):
        text = state.get('text').format(**state)
        return Doc(
            Html(
                Body(
                    P(text),
                    Ul(*[Li(A(o.option_text, href=f'{l}.html')) for l, o in option_links])
                )
            )     
        )

    def render(self, start=True, **state):
        if start:
            for root, _, files in os.walk("build"):
                for file in files:
                    os.remove(os.path.join(root, file))

        new_state = {**state, **self.state}
        if self.updater:
            new_state = self.updater(new_state)
        
        page_hash = f'{abs(int(hash(str(self.id) + str(new_state))))}'
        is_cached = page_hash in self._cache
        self._cache.append(page_hash)
        if not is_cached:
            hashes = [(o.render(**new_state, start=False), o) for o in self.options]
            content = self.template(new_state, hashes)
            filename = 'index.html' if start else f'{page_hash}.html'
            with open(f'build/{filename}', 'w') as f:
                f.write(str(content))
        return page_hash
