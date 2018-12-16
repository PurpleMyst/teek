import time
from types import SimpleNamespace

import pytest
import pythotk as tk


def run_event_loop(for_how_long):
    # this is dumb
    start = time.time()
    while time.time() < start + for_how_long:
        tk.update()


@pytest.mark.slow
def test_set_tooltip():
    window = tk.Window()
    assert not hasattr(window, '_tooltip_manager')

    tk.extras.set_tooltip(window, None)
    assert not hasattr(window, '_tooltip_manager')

    tk.extras.set_tooltip(window, 'Boo')
    assert window._tooltip_manager.text == 'Boo'

    tk.extras.set_tooltip(window, None)
    assert window._tooltip_manager.text is None

    tk.extras.set_tooltip(window, 'lol')
    assert window._tooltip_manager.text == 'lol'

    assert not window._tooltip_manager.got_mouse
    window._tooltip_manager.enter(SimpleNamespace(widget=window))
    assert window._tooltip_manager.got_mouse
    window._tooltip_manager.motion(SimpleNamespace(rootx=123, rooty=456))
    assert window._tooltip_manager.mousex == 123
    assert window._tooltip_manager.mousey == 456

    run_event_loop(1.1)
    assert window._tooltip_manager.tipwindow is not None
    assert window._tooltip_manager.got_mouse
    window._tooltip_manager.leave(SimpleNamespace(widget=window))
    assert not window._tooltip_manager.got_mouse
    assert window._tooltip_manager.tipwindow is None

    # what happens if the window gets destroyed before it's supposed to show?
    window._tooltip_manager.enter(SimpleNamespace(widget=window))
    window._tooltip_manager.leave(SimpleNamespace(widget=window))
    assert window._tooltip_manager.tipwindow is None
    run_event_loop(1.1)
    assert window._tooltip_manager.tipwindow is None

