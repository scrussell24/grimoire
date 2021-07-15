import os
from copy import copy
from inspect import signature


os.environ["PYTHONHASHSEED"] = "0"


class Page:
    def __init__(self, fn):
        self.fn = fn
        self.cache = []

    def render(self, state, pages, path, start=True):

        # clear out the dir
        if start:
            for root, _, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))

        # calc page hash
        page_hash = f"{abs(hash(hash(self) + hash(str(state))))}"

        if page_hash not in self.cache:
            self.cache.append(page_hash)

            # find the option pages we'll need to inject
            params = signature(self.fn).parameters
            options = []
            for name, page in pages.items():
                if name in params.keys():
                    options.append(page)

            # render with the state so we can render the children (we're going to have to do this again)
            _, new_state = self.fn(copy(state), *["" for _ in range(len(params) - 1)])

            # render the children
            child_hashes = []
            for page in options:
                child_hash = page.render(copy(new_state), pages, path, start=False)
                child_hashes.append(child_hash)

            # render this page again with the correct children hashes
            content, state = self.fn(copy(state), *child_hashes)

            # write the file to the build dir
            filename = f"{page_hash}.html"
            with open(f"{path}{filename}", "w") as f:
                f.write(str(content))

            # if it's the first page also write an index file
            if start:
                with open(f"{path}index.html", "w") as f:
                    f.write(str(content))

        return page_hash


class Grimoire:
    def __init__(self, state=None):
        self.pages = {}
        self.start = None
        self.state_class = state

    def page(self, start=False):
        def inner(f):
            page = Page(f)
            if start:
                self.start = page
            self.pages[f.__name__] = page
            return f

        return inner

    def render(self, path="site/"):
        if not self.start:
            raise Exception(
                "No start page set. Make sure to add a start=True argument to your first page."
            )
        state = self.state_class() if self.state_class else {}
        self.start.render(state, self.pages, path)
