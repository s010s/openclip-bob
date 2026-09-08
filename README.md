# Bob for OpenClip

Translate selected text with [Bob](https://bobtranslate.com/) from the [OpenClip](https://github.com/ganeshmshetty/openclip) selection menu.

**Select text → click Translate with Bob → read the result in Bob.**

This small AppleScript extension keeps your existing Bob translation services and shows Bob's window near your pointer. No extra translation API keys or build step are required.

## Install

1. Install OpenClip and the Mac App Store edition of Bob.
2. Download **Bob.openclipext.zip** from [Releases](https://github.com/s010s/openclip-bob/releases/latest).
3. Extract the folder into `~/.openclip/extensions/`, reload OpenClip, and enable **Translate with Bob** in Actions.
4. Allow OpenClip to control Bob when macOS asks on first use.

Tested locally with OpenClip 1.3.1 and Bob 1.20.0, including actual selection-to-translation use. See the [extension guide](Bob.openclipext/README.md) for requirements, privacy, troubleshooting, and prototype migration.

## Independent release and official catalog

This repository is the source of truth. Independent releases contain the same extension files submitted to the OpenClip catalog. Catalog inclusion is subject to upstream review; publishing here does not automatically mean store availability.

The **Submit to OpenClip catalog** workflow opens a version-specific upstream PR after a stable release is published. It can also be rerun manually. It requires a cross-repository secret; see [maintenance instructions](MAINTAINING.md).

## Development

On macOS:

```sh
python3 scripts/test.py
python3 scripts/package.py
```

The tests exercise the AppleScript serializer without sending text to Bob. The package builder includes only an explicit list of extension files, including the Bob SVG icon, its original source image, and third-party license notices. CI uploads a ZIP artifact; it does not publish a release on every push.

## License

Integration code: [MIT](LICENSE). Bob icon: [GPL-3.0, with source attribution](Bob.openclipext/THIRD_PARTY_NOTICES.md). Independent integration by [s010s](https://github.com/s010s), not affiliated with Bob or OpenClip. Bob is installed separately; its license and translation service charges are unaffected.
