#!/usr/bin/env python
import sys
import string

indexes = [0, 2, 3, 4]
sys.stdin.readline()
for line in sys.stdin:
    line = line.strip()
    values = line.split(',')
    values = values[0:5]
    print(*values, sep=',')