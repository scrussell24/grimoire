import os
from copy import copy
from pathlib import Path
from string import Template
from inspect import signature
from os.path import isfile, join


from grimoire.errors import GrimoireUnknownPageOptions, GrimoireNoStartPage


os.environ["PYTHONHASHSEED"] = "0"


class Page:
    def __init__(self, fn):
        self.fn = fn
        self.cache = []

    def page_number(self, page_hash):
        return f"{self.fn.__name__}_{self.cache.index(page_hash)}"

    def render(self, state, pages, path, start=True):

        # clear out the dir of html files
        if start:
            Path(path).mkdir(parents=True, exist_ok=True)
            html_files = [
                f
                for f in os.listdir(path)
                if isfile(join(path, f)) and f.endswith(".html")
            ]
            for file in html_files:
                os.remove(os.path.join(path, file))

        # calc page hash
        page_hash = f"{abs(hash(hash(self) + hash(str(state))))}"

        if page_hash not in self.cache:
            # This page/state has not yet been rendered
            self.cache.append(page_hash)

            # find the option pages we'll need to inject
            params = list(signature(self.fn).parameters.keys())
            used_params = []
            options = []
            for name, page in pages.items():
                if name in params:
                    used_params.append(name)
                    options.append(page)

            # Make sure a page functions exist for all parameters (besides state)
            unused_params = set(params[1:]).difference(set(used_params))
            if unused_params:
                raise GrimoireUnknownPageOptions(unused_params)

            # render, inject the option name which will
            # be replaced with the actual hash later
            content, new_state = self.fn(
                copy(state), *[f"${k}" for k in list(params)[1:]]
            )

            # render the children
            page_ids = {}
            for page in options:
                child_page_id = page.render(copy(new_state), pages, path, start=False)
                page_ids[page.fn.__name__] = child_page_id

            # inject the real child page id's into this page o
            template = Template(str(content))
            content = template.substitute(page_ids)

            # write the file to the build dir
            filename = f"{self.page_number(page_hash)}.html"
            with open(f"{path}{filename}", "w") as f:
                f.write(content)

            # if it's the first page also write an index file
            if start:
                with open(f"{path}index.html", "w") as f:
                    f.write(content)

        return self.page_number(page_hash)


class Grimoire:
    def __init__(self, state=None):
        self.pages = {}
        self.start = None
        self.state_class = state

    def page(self, start: bool = False):
        def inner(f):
            page = Page(f)
            if start:
                self.start = page
            self.pages[f.__name__] = page
            return f

        return inner

    def render(self, path: str = "site/"):
        if not self.start:
            raise GrimoireNoStartPage()
        state = self.state_class() if self.state_class else {}
        self.start.render(state, self.pages, path)
