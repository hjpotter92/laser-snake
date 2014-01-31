#!/usr/bin/env python
import os
import re

files = [f for f in os.listdir('.') if os.path.isfile(f)]
patterns = [r'#.*#', r'.*~', r'.*\.pyc']
to_del = []
for p in patterns:
	to_del += filter(lambda x: re.search(p, x) != None, files)

for f in to_del:
	if os.path.isfile(f):os.remove(f)
