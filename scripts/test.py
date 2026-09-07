#!/usr/bin/env python3
"""Check the real AppleScript serializer without invoking Bob or sending events."""
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
script = (root / 'Bob.openclipext/translate.applescript').read_text()
# Keep the production serialization code and stop before the external app call.
probe = script.split('tell application id ')[0] + '\nreturn requestJSON\n'
cases = ['中文 😀\t{query}\r\nSecond line: "quotes" and \\ path', 'Long text. ' * 5000]
for value in cases:
    escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')
    source = f'property OPENCLIP_TEXT : "{escaped}"\n' + probe
    result = subprocess.run(['osascript', '-e', source], check=True, capture_output=True, text=True)
    request = json.loads(result.stdout)
    assert request == {'path': 'translate', 'body': {'action': 'translateText', 'text': value, 'windowLocation': 'mouse'}}
assert script.rstrip().endswith('return ""')
print('PASS: Unicode, newlines, quotes, backslashes, placeholders, long-text serialization; empty result contract.')
