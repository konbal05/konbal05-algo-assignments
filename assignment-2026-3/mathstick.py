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

class MatchstickSolver:
    def __init__(self, problem, max_k):
        match = EQUATION_RE.match(problem)
        if not match:
            raise ValueError("invalid problem")
        self.n1, self.op, self.n2, self.n3 = match.groups()
        self.max_k = max_k
        self.digits = [int(ch) for ch in self.n1 + self.n2 + self.n3]
        self.w1 = len(self.n1)
        self.w2 = len(self.n2)
        self.ns = len(self.digits)
        self.letters = [chr(ord("A") + i) for i in range(self.ns)]
        self.candidates = [digit_candidates(d, max_k) for d in self.digits]
        self.suf_min = [0] * (self.ns + 1)
        self.suf_max = [0] * (self.ns + 1)
        for i in range(self.ns - 1, -1, -1):
            deltas = [c.add - c.remove for c in self.candidates[i]]
            self.suf_min[i] = self.suf_min[i + 1] + min(deltas)
            self.suf_max[i] = self.suf_max[i + 1] + max(deltas)
        self.chosen = [0] * self.ns
        self.visited = 0
        self.pruned = 0
        self.results = []
        
