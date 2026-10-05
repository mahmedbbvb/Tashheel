import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('lecture.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    s = line.strip()
    if 'mcq-q' in s or ('checkMCQ' in s and 'mcq-letter' in s) or ('mcq-explain' in s and 'id=' in s):
        print(i, s[:130])
