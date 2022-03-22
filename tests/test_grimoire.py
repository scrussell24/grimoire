import builtins
from dataclasses import dataclass

import pytest
import grimoire

from grimoire.core import Grimoire
from grimoire.templates import default_page, link
from grimoire.errors import GrimoireInvalidOption, GrimoireUnknownPageOptions, GrimoireNoStartPage


Grimoire = grimoire.Grimoire


@pytest.fixture
def mock_open():
    class MockFile:
        def __init__(self):
            self.called = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            ...

        def write(self, content):
            self.called.append(("write", (content,), {}))
            ...

        def called_with(self, method, *args, **kwargs):
            for call in self.called:
                if method == call[0] and args == call[1] and kwargs == call[2]:
                    return True

    class MockOpen:
        def __init__(self):
            self.files = {}

        def __call__(self, filename, *args, **kwargs):
            mock_file = MockFile()
            self.files[filename] = mock_file
            return mock_file

        def get_file(self, filename):
            return self.files[filename]

    return MockOpen()


@dataclass
class State:
    test: str = ""


def test_sanity():
    assert True


def test_create_app():
    Grimoire()


def test_create_app_with_state():
    Grimoire(State)


def test_create_app_with_state_kwarg():
    Grimoire(state=State)


def test_render_with_no_first_page():
    with pytest.raises(GrimoireNoStartPage) as err:
        app = Grimoire()
        app.render()


def test_render_with_first_page(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state):
        return "Test", state

    app.render()

    assert mock_open.get_file("site/index.html").called_with("write", "Test")


def test_render_with_custom_dir(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state):
        return "Test", state

    app.render("app/")

    assert mock_open.get_file("app/index.html").called_with("write", "Test")


def test_render_with_child_page(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state, second):
        return "Test", state

    @app.page()
    def second(state):
        return "second page", state

    app.render()

    assert mock_open.get_file("site/index.html").called_with("write", "Test")
    assert mock_open.get_file("site/second_0.html").called_with("write", "second page")


def test_render_with_multiple_child_pages(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state, second, third):
        return "Test", state

    @app.page()
    def second(state):
        return "second page", state

    @app.page()
    def third(state):
        return "third page", state

    app.render()

    assert mock_open.get_file("site/index.html").called_with("write", "Test")
    assert mock_open.get_file("site/second_0.html").called_with("write", "second page")
    assert mock_open.get_file("site/third_0.html").called_with("write", "third page")


def test_render_link_to_child(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state, second):
        return f"Test, go to {second}", state

    @app.page()
    def second(state):
        return "second page", state

    app.render()
    assert mock_open.get_file("site/index.html").called_with(
        "write", "Test, go to second_0"
    )
    assert mock_open.get_file("site/second_0.html").called_with("write", "second page")


def test_render_link_to_parent(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state, second):
        return f"Test, go to {second}", state

    @app.page()
    def second(state, start):
        return f"second page, go to {start}", state

    app.render()
    assert mock_open.get_file("site/index.html").called_with(
        "write", "Test, go to second_0"
    )
    assert mock_open.get_file("site/second_0.html").called_with(
        "write", "second page, go to start_0"
    )


def test_render_with_default_template(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    @default_page("Title")
    def start(state, second):
        return "Test", [], state

    @app.page()
    @default_page("Title")
    def second(state):
        return "second page", [], state

    app.render()


def test_state(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire(State)

    @app.page(start=True)
    def start(state, second):
        state.test = "test state"
        return f"Test, go to {second}", state

    @app.page()
    def second(state):
        return f"second page, {state.test}", state

    app.render()
    assert mock_open.get_file("site/index.html").called_with(
        "write", "Test, go to second_0"
    )
    assert mock_open.get_file("site/second_0.html").called_with(
        "write", "second page, test state"
    )


def test_render_the_same_page_multiple_times(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire(State)

    @app.page(start=True)
    def start(state, second, third):
        return "Test", state

    @app.page()
    def second(state, fourth):
        state.test = "went to second page"
        return "second page", state

    @app.page()
    def third(state, fourth):
        state.test = "went to third page"
        return "third page", state

    @app.page()
    def fourth(state):
        return state.test, state

    app.render()

    assert mock_open.get_file("site/index.html").called_with("write", "Test")
    assert mock_open.get_file("site/second_0.html").called_with("write", "second page")
    assert mock_open.get_file("site/third_0.html").called_with("write", "third page")
    assert mock_open.get_file("site/fourth_0.html").called_with(
        "write", "went to second page"
    )
    assert mock_open.get_file("site/fourth_1.html").called_with(
        "write", "went to third page"
    )


def test_render_invalid_option(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state):
        return f"Test, go to {link('second', second)}", state

    @app.page()
    def second(state):
        return "second page", state

    with pytest.raises(GrimoireInvalidOption):
        app.render()


def test_render_unknown_options(monkeypatch, mock_open):
    monkeypatch.setattr(builtins, "open", mock_open)

    app = Grimoire()

    @app.page(start=True)
    def start(state, third):
        return f"Test, go to {link('second', third)}", state

    @app.page()
    def second(state):
        return "second page", state

    with pytest.raises(GrimoireUnknownPageOptions):
        app.render()
