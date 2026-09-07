# Releases and catalog synchronization

## One source, two channels

Keep the extension in `Bob.openclipext/`. Use the same identifier (`io.github.s010s.openclip.bob`), version, and four packaged files for independent releases and the official catalog. Never include internal working notes in a release or PR.

## One-time automation setup

The fork `s010s/openclip-extensions` receives version branches; PRs target `ganeshmshetty/openclip-extensions:main`.

Set an Actions repository secret named **OPENCLIP_SYNC_TOKEN** in `s010s/openclip-bob`. The token must be able to push contents to the fork and create pull requests in the public upstream repository. The ordinary workflow `GITHUB_TOKEN` is scoped to this repository and cannot do both operations. Choose a credential that actually supports this cross-owner contribution flow; a classic PAT with `public_repo` is one option, but grants broad public-repository write access. Do not assume a fine-grained token limited to the fork can create upstream PRs. Prefer a dedicated expiring credential, and rotate it when needed. Never put tokens in files, workflow inputs, logs, or issues.

Forked copies of this project do not run the submission job. The workflow has read-only built-in token permissions, and receives the synchronization credential only in the necessary steps. It runs only for releases or a manual dispatch, not for pull requests.

## Publish a version

1. Update the manifest version and user documentation; verify actual behavior when script logic changes.
2. Run `python3 scripts/test.py` on macOS and the official catalog's `scripts/validate.sh Bob.openclipext`.
3. Run `python3 scripts/package.py`. Inspect the staged files and ZIP contents before public publication.
4. Commit and tag the reviewed source as `vX.Y.Z`, then publish a stable GitHub Release containing `dist/Bob.openclipext.zip` and `dist/SHA256SUMS`.
5. The release event runs **Submit to OpenClip catalog**. The manifest version must match the release tag. The script validates against the current upstream validator before pushing only the four extension files to `bob/vX.Y.Z` in the fork.
6. Review CI and respond to maintainer feedback. Upstream review and merging remain human decisions. The workflow does not merge PRs.

If the release was created through an API using a workflow's own GITHUB_TOKEN, GitHub may suppress follow-on workflow events. Manually dispatch the catalog workflow with the published tag in that case.

## Retries and review feedback

Manual dispatch with the same tag reuses the version branch and PR rather than creating duplicates or force-pushing. Existing PR bodies and reviewer discussion are preserved. A closed or merged PR is reported and is not reopened automatically. For a new version, publish a new release.

If setup is incomplete, the workflow fails with a missing-secret message. After adding the secret, rerun with the published tag. A local authenticated `gh` session can also run `scripts/sync_catalog.py` with GH_TOKEN supplied through the environment; never print the token.
