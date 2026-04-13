"""Prototype accumulator for circle voting — standalone scratch, not integrated."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass
class HoughScratch:
    bins: Dict[Tuple[int, int, int], float] = field(default_factory=dict)

    def vote(self, a: int, b: int, r: int, w: float = 1.0) -> None:
        key = (a // 3, b // 3, max(1, r // 2))
        self.bins[key] = self.bins.get(key, 0.0) + w

    def peak(self) -> Optional[Tuple[Tuple[int, int, int], float]]:
        if not self.bins:
            return None
        return max(self.bins.items(), key=lambda kv: kv[1])
