import os
from uuid import uuid4

from hype import *


os.environ['PYTHONHASHSEED'] = "0"


class Page:
    text = ""
    option_text = ""
    options = ()
    _cache = []

    def __init__(
        self,
        text=None,
        options=None,
        option_text=None,
        **state
    ):
        self.state = state
        self.text = text if text else self.text
        self.options = options if options else self.options
        self.option_text = option_text if option_text else self.option_text
        self.id = uuid4()

    def render(self, start=True, **state):
        # clear out build dir
        if start:
            for root, _, files in os.walk("build"):
                for file in files:
                    os.remove(os.path.join(root, file))
        new_state = {**state, **self.state}
        formatted_text = self.text.format(**new_state)
        page_hash = f'{hash(str(self.id) + str(new_state))}'
        is_cached = page_hash in self._cache
        self._cache.append(page_hash)
        if not is_cached:
            hashes = [(o.render(**new_state, start=False), o) for o in self.options]
            content = Doc(
                Html(
                    Body(
                        P(formatted_text),
                        Ul(*[Li(A(o.option_text, href=f'{h}.html')) for h, o in hashes])
                    )
                )     
            )
            filename = 'index.html' if start else f'{page_hash}.html'
            with open(f'build/{filename}', 'w') as f:
                f.write(str(content))
        return page_hash
