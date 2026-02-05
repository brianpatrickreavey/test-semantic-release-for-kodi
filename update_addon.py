#!/usr/bin/env python3
import subprocess
import re
import sys
import os
from jinja2 import Template
from pathlib import Path

# Debugging: Print environment details
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {Path.cwd()}")
print(f"sys.path: {sys.path}")
print(f"Environment PATH: {os.environ.get('PATH', 'Not set')}")

# Get the latest version from pyproject.toml
with open('pyproject.toml', 'r') as f:
    content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    version = match.group(1) if match else "0.1.0"

# Whitelist of commit types to include in addon.xml news
# Standard conventional commits: feat, fix, perf, refactor, docs, style, test, chore, ci, build, revert
# For addon.xml, we include only user-facing changes: feat and fix, as well as perf.
included_types = ['feat', 'fix', 'perf']

# Get commits since last tag
result = subprocess.run(['git', 'log', '--oneline', '--pretty=format:%s', 'HEAD...v0.1.0'], capture_output=True, text=True)
commits = []
for line in result.stdout.strip().split('\n'):
    if line:
        # Parse type from commit message
        match = re.match(r'(\w+): (.+)', line)
        if match:
            type_ = match.group(1)
            subject = match.group(2)
            # Only include whitelisted types
            if type_ in included_types:
                commits.append({'type': type_, 'subject': subject})

# Sort commits: feat/perf first, then fix, etc.
priority = {'feat': 0, 'perf': 0, 'fix': 1}
commits.sort(key=lambda c: priority.get(c['type'], 99))

# Render template
template_path = Path('templates/addon.xml.j2')
with open(template_path, 'r') as f:
    template = Template(f.read())

output = template.render(version=version, commits=commits)

# Write to addon.xml
with open('addon.xml', 'w') as f:
    f.write(output)

print(f"Updated addon.xml to version {version}")