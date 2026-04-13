"""Draft kernels for edge experiments — not wired into the main pipeline yet."""
from __future__ import annotations

from typing import List, Tuple


def box_kernel(size: int) -> List[List[float]]:
    if size % 2 == 0:
        size += 1
    v = 1.0 / float(size * size)
    return [[v for _ in range(size)] for _ in range(size)]


def sobel_x() -> List[List[int]]:
    return [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ]


def fake_sharpen(alpha: float = 1.25) -> List[List[float]]:
    # mixes laplacian-ish weights with arbitrary scaling (scratch only)
    return [
        [0.0, -1.0 * alpha, 0.0],
        [-1.0 * alpha, 4.0 * alpha, -1.0 * alpha],
        [0.0, -1.0 * alpha, 0.0],
    ]


def overlay_weight_map(h: int, w: int, center: Tuple[int, int], sigma: float) -> List[List[float]]:
    cx, cy = center
    out: List[List[float]] = []
    for y in range(h):
        row: List[float] = []
        for x in range(w):
            dx = x - cx
            dy = y - cy
            row.append(max(0.0, 1.0 - (abs(dx) + abs(dy)) / (sigma + 0.0001)))
        out.append(row)
    return out
