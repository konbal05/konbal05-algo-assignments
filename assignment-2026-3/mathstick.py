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
        a = len(dst - src)
        r = len(src - dst)
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

def solve(self):
        for target_op in ("+", "-"):
            self.op_add = 1 if (self.op == "-" and target_op == "+") else 0
            self.op_remove = 1 if (self.op == "+" and target_op == "-") else 0
            if self.op_add > self.max_k or self.op_remove > self.max_k:
                continue
            self.target_op = target_op
            self.required_net = self.op_remove - self.op_add
            self._search(0, 0, 0)
        return self._build_summary()

    def _search(self, slot, sticks_added, sticks_removed):
        self.visited += 1
        if slot == self.ns:
            self._record(sticks_added)
            return
        for c in self.candidates[slot]:
            ta = sticks_added + c.add
            tr = sticks_removed + c.remove
            if ta + self.op_add > self.max_k or tr + self.op_remove > self.max_k:
                self.pruned += 1
                continue
            remaining = self.required_net - (ta - tr)
            if not (self.suf_min[slot + 1] <= remaining <= self.suf_max[slot + 1]):
                self.pruned += 1
                continue
            self.chosen[slot] = c.target
            self._search(slot + 1, ta, tr)

