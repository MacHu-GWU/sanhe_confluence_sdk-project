# -*- coding: utf-8 -*-

from rich import print as rprint
from varname import argname


def debug_prop(v):
    print(f"\n--- {argname('v')}")
    rprint(v)
