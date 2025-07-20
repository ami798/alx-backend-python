#!/usr/bin/env python3
"""Utils module containing utility functions."""

from typing import Mapping, Any, Sequence, Union
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """Get JSON from an API URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Memoization decorator."""
    attr_name = "_{}".format(fn.__name__)

    @property
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
