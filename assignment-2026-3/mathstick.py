import argparse
import json
import re
import sys
from collections import namedtuple

Candidate = namedtuple('Candidate', ['target', 'add', 'remove'])

DIGIT_SEGMENTS = {
    0: {1, 2, 3, 4, 5, 6},
    1: {2, 3},
    2: {0, 1, 2, 4, 5},
    3: {0, 1, 2, 3, 4},
    4: {0, 2, 3, 6},
    5: {0, 1, 3, 4, 6},
    6: {0, 1, 3, 4, 5, 6},
    7: {1, 2, 3, 6},
    8: {0, 1, 2, 3, 4, 5, 6},
    9: {0, 1, 2, 3, 4, 6},
}

OP_SEGMENT = "OP0"

EQUATION_RE = re.compile(r"^\s*(\d+)\s*([+-])\s*(\d+)\s*=\s*(\d+)\s*$")

def digit_candidates(digit, max_k):
    src = DIGIT_SEGMENTS[digit]
    result = []
    for tgt, dst in DIGIT_SEGMENTS.items():
        a = len(dst - src)   # σπίρτα που προστίθενται
        r = len(src - dst)   # σπίρτα που αφαιρούνται
        if a <= max_k and r <= max_k:
            result.append(Candidate(tgt, a, r))
    result.sort(key=lambda c: (c.add + c.remove, c.target))
    return result


def _equation_holds(v1, op, v2, v3):
    if op == "+":
        return v1 + v2 == v3
    return v1 - v2 == v3
