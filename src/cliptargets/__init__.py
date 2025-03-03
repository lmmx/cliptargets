"""Enumerate multiple clipboard targets.

This package provides functions to enumerate and retrieve the values of
various clipboard targets/formats using xclip.
"""

__version__ = "0.1.1"

from .core import get_all_targets, get_target_value, get_targets

__all__ = ["get_all_targets", "get_target_value", "get_targets"]
