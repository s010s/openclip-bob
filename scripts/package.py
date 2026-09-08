#!/usr/bin/env python3
"""Build a distributable containing only the reviewed extension files."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('openclip.json', 'translate.applescript', 'README.md', 'LICENSE', 'icon.svg', 'icon-source.png', 'THIRD_PARTY_NOTICES.md', 'LICENSE.icon-GPL-3.0')

def main():
    package = ROOT / 'Bob.openclipext'
    manifest = json.loads((package / 'openclip.json').read_text())
    assert manifest['identifier'] == 'io.github.s010s.openclip.bob'
    assert manifest['actions'][0]['script'] == 'translate.applescript'
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    archive = output / 'Bob.openclipext.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name in FILES:
            info = zipfile.ZipInfo(f'Bob.openclipext/{name}', (2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (package / name).read_bytes())
    (output / 'SHA256SUMS').write_text(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n')
    print(archive)

if __name__ == '__main__':
    main()
