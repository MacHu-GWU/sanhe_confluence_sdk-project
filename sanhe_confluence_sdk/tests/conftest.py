# -*- coding: utf-8 -*-

import pytest

from sanhe_confluence_sdk.tests import debugger


@pytest.fixture
def mute():
    """Fixture to mute debug_prop output during test execution."""
    with debugger.mute():
        yield
