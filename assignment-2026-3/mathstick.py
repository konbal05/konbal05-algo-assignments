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
            
def _record(self, sticks_added):
        moves = sticks_added + self.op_add
        if moves < 1:
            return
        e1 = "".join(str(d) for d in self.chosen[:self.w1])
        e2 = "".join(str(d) for d in self.chosen[self.w1:self.w1 + self.w2])
        e3 = "".join(str(d) for d in self.chosen[self.w1 + self.w2:])
        if not _equation_holds(int(e1), self.target_op, int(e2), int(e3)):
            return
        picks, places = [], []
        for i in range(self.ns):
            src = DIGIT_SEGMENTS[self.digits[i]]
            dst = DIGIT_SEGMENTS[self.chosen[i]]
            picks  += ["{}{}".format(self.letters[i], s) for s in sorted(src - dst)]
            places += ["{}{}".format(self.letters[i], s) for s in sorted(dst - src)]
        if self.op_remove:
            picks.append(OP_SEGMENT)
        if self.op_add:
            places.append(OP_SEGMENT)
        self.results.append((moves, {
            "equation": "{} {} {} = {}".format(e1, self.target_op, e2, e3),
            "picks":  picks,
            "places": places,
            "moves":  ["Move({}, {})".format(p, q) for p, q in zip(picks, places)],
            "nodes_visited": self.visited,
            "nodes_pruned": self.pruned,
        }))

    def _build_summary(self):
        counts = {str(k): 0 for k in range(1, self.max_k + 1)}
        sols   = {str(k): [] for k in range(1, self.max_k + 1)}
        for moves, sol in self.results:
            key = str(moves)
            counts[key] += 1
            sols[key].append(sol)
        for bucket in sols.values():
            bucket.sort(key=lambda s: s["equation"])
        return {
            "problem":       "{} {} {} = {}".format(self.n1, self.op, self.n2, self.n3),
            "max_k":         self.max_k,
            "counts":        counts,
            "nodes_visited": self.visited,
            "nodes_pruned":  self.pruned,
            "solutions":     sols,
        }
