#!/usr/bin/env python

import subprocess

result = subprocess.run(
    ["mpremote", "a0", "fs", "ls", ":"], 
    capture_output=True,
    text = True
)

lines = result.stdout.splitlines()

for line in lines[:-1]:
    file = line.strip().split(' ')[1]
    subprocess.run(
        ["mpremote", "a0", "fs", "cp", ":" + file, "."]
    )
    print(file)

