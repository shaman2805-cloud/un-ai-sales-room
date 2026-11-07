#!/bin/zsh
set -eu
cd -- "${0:A:h}"
if command -v python3 >/dev/null 2>&1; then
  task_python="$(command -v python3)"
elif [[ -x /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 ]]; then
  task_python=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
else
  print 'Python 3.10 or newer is required. Download it from python.org.'
  read '?Press Enter to close.'
  exit 1
fi
exec "$task_python" -m salesroom serve --open
