#!/usr/bin/env python3
"""Backward-compatible shim — use skillhub.recommend instead."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from skillhub.recommend import *  # noqa: F403
