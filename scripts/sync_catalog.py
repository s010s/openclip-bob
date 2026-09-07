#!/usr/bin/env python3
"""Open/update a version-specific catalog PR from a published release checkout."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = 'ganeshmshetty/openclip-extensions'
FORK = 's010s/openclip-extensions'
FILES = ('openclip.json', 'translate.applescript', 'README.md', 'LICENSE')

def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

def main():
    if not os.environ.get('GH_TOKEN'):
        raise SystemExit('Configure the OPENCLIP_SYNC_TOKEN repository secret. Never pass credentials as workflow inputs.')
    package_root = Path(os.environ.get('PACKAGE_ROOT', str(ROOT))).resolve()
    manifest = json.loads((package_root / 'Bob.openclipext/openclip.json').read_text())
    version = manifest['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise SystemExit('Expected a stable semantic version.')
    tag = os.environ.get('RELEASE_TAG', f'v{version}')
    if tag != f'v{version}':
        raise SystemExit('Release tag and manifest version do not match.')
    release = json.loads(run('gh', 'release', 'view', tag, '--repo', 's010s/openclip-bob', '--json', 'isDraft,isPrerelease,url'))
    if release['isDraft'] or release['isPrerelease']:
        raise SystemExit('Only published stable releases may be submitted.')
    branch = f'bob/v{version}'
    with tempfile.TemporaryDirectory(prefix='bob-catalog-') as temp:
        checkout = Path(temp) / 'catalog'
        run('gh', 'repo', 'clone', FORK, str(checkout), '--', '--depth', '1')
        remotes = run('git', 'remote', cwd=checkout).splitlines()
        operation = 'set-url' if 'upstream' in remotes else 'add'
        run('git', 'remote', operation, 'upstream', f'https://github.com/{UPSTREAM}.git', cwd=checkout)
        run('git', 'fetch', 'upstream', 'main', '--depth', '1', cwd=checkout)
        existing = run('git', 'ls-remote', '--heads', 'origin', f'refs/heads/{branch}', cwd=checkout)
        if existing:
            run('git', 'fetch', 'origin', branch, '--depth', '1', cwd=checkout)
            run('git', 'checkout', '-b', branch, 'FETCH_HEAD', cwd=checkout)
        else:
            run('git', 'checkout', '-b', branch, 'upstream/main', cwd=checkout)
        target = checkout / 'raw/Bob.openclipext'
        target.mkdir(parents=True, exist_ok=True)
        for name in FILES:
            shutil.copyfile(package_root / 'Bob.openclipext' / name, target / name)
        run('bash', 'scripts/validate.sh', 'raw/Bob.openclipext', cwd=checkout)
        run('git', 'config', 'user.name', 's010s', cwd=checkout)
        run('git', 'config', 'user.email', 's010s@users.noreply.github.com', cwd=checkout)
        run('git', 'add', '--', *[f'raw/Bob.openclipext/{name}' for name in FILES], cwd=checkout)
        changed = run('git', 'diff', '--cached', '--name-only', cwd=checkout)
        if changed:
            allowed = {f'raw/Bob.openclipext/{name}' for name in FILES}
            if not set(changed.splitlines()) <= allowed:
                raise SystemExit('Unexpected staged files; refusing to publish.')
            run('git', 'commit', '-m', f'Add/update Bob extension to {version}', cwd=checkout)
            run('git', 'push', 'origin', f'HEAD:refs/heads/{branch}', cwd=checkout)
        prs = json.loads(run('gh', 'pr', 'list', '--repo', UPSTREAM, '--head', f's010s:{branch}', '--state', 'all', '--json', 'url,state'))
        if prs:
            print(f'Existing PR ({prs[0]["state"]}): {prs[0]["url"]}; preserving reviewer discussion and body.')
            return
        if not changed and not existing:
            print('Catalog already matches this release; no PR needed.')
            return
        body = (ROOT / '.github/catalog-pr.md').read_text().replace('{{VERSION}}', version).replace('{{RELEASE_URL}}', release['url'])
        body_path = Path(temp) / 'pr.md'
        body_path.write_text(body)
        print(run('gh', 'pr', 'create', '--repo', UPSTREAM, '--base', 'main', '--head', f's010s:{branch}', '--title', f'Add/update Bob extension (v{version})', '--body-file', str(body_path)))

if __name__ == '__main__':
    main()
