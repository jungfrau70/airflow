#!/usr/bin/python
import re
import subprocess

# Open the file for reading
with open('test.env', 'r') as f:
    contents = f.read()

# Find all occurrences of the string followed by a number
pattern = re.compile(r'tp=(\d+)')
matches = pattern.findall(contents)

# Replace each match with the number that follows it
tp = 0.3
newstring = str(tp)
for match in matches:
    contents = contents.replace(f'{match}', newstring)

# Write the modified contents back to the file
with open('test.env', 'w') as f:
    f.write(contents)
