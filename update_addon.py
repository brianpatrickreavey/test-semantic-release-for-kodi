#!/usr/bin/env python3
import subprocess
import re
from jinja2 import Template
from pathlib import Path

# Get the latest version from pyproject.toml
with open('pyproject.toml', 'r') as f:
    content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    version = match.group(1) if match else "0.1.0"

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
            commits.append({'type': type_, 'subject': subject})

# Render template
template_path = Path('templates/addon.xml.j2')
with open(template_path, 'r') as f:
    template = Template(f.read())

output = template.render(version=version, commits=commits)

# Write to addon.xml
with open('addon.xml', 'w') as f:
    f.write(output)

print(f"Updated addon.xml to version {version}")