# -*- coding: utf-8 -*-

from contextlib import contextmanager

from rich import print as rprint
from varname import argname


class Debugger:
    """
    A debugger utility for printing property values during testing.

    Supports muting output via context manager, useful for suppressing
    verbose output in automated tests while keeping it available for
    interactive debugging.
    """

    def __init__(self):
        self._muted = False

    @property
    def muted(self) -> bool:
        return self._muted

    @contextmanager
    def mute(self):
        """Context manager to temporarily mute debug output."""
        original = self._muted
        self._muted = True
        try:
            yield
        finally:
            self._muted = original

    def print(self, v):
        """Print a value with its variable name, unless muted."""
        if not self._muted:
            print(f"\n--- {argname('v', frame=2)}")
            rprint(v)


# Global debugger instance
debugger = Debugger()


def debug_prop(v):
    """Convenience function that delegates to the global debugger."""
    if not debugger.muted:
        print(f"\n--- {argname('v')}")
        rprint(v)
