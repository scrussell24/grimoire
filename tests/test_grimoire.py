from dataclasses import dataclass

from grimoire import Grimoire


@dataclass
class State:
    test: str


def test_sanity():
    assert True


def test_create_app():
    app = Grimoire()
    assert app


def test_create_app_with_state():
    app = Grimoire(State)
    assert app


def test_create_app_with_state_kwarg():
    app = Grimoire(state=State)
    assert app
