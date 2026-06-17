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
