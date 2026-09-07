### Extension Summary

- **Name**: Bob
- **Type**: [ ] JavaScript / [ ] URL Template / [ ] Shell / [x] AppleScript
- **Identifier**: `io.github.s010s.openclip.bob`
- **Version**: {{VERSION}}
- **Source and support**: https://github.com/s010s/openclip-bob
- **Independent release**: {{RELEASE_URL}}

### Description

[Bob](https://bobtranslate.com/) is a macOS translation and OCR application. It lets users configure their preferred translation services and dictionaries in one place. This extension adds one focused action, **Translate with Bob**: select text, click the OpenClip action, and read the translation in Bob's own window near the pointer. It reuses the user's existing Bob configuration. OCR and additional translation actions are outside this extension's scope.

#### Why I built this

I previously used PopClip mainly together with Bob for selected-text translation. The two-year license I had purchased for PopClip expired, and I decided to move to OpenClip. I wanted to keep the Bob workflow I was already comfortable with, so I built this small integration. After allowing the expected macOS Automation permission, I tested it locally and confirmed that selecting text and translating it with Bob works.

#### Implementation and permissions

- Uses Bob's [documented AppleScript request interface](https://bobtranslate.com/guide/integration/applescript.html): `translateText`, with `windowLocation: "mouse"`.
- Passes `OPENCLIP_TEXT` directly through Foundation JSON serialization. It does not simulate a keyboard shortcut or ask Bob to recapture the selection after focus changes.
- Uses AppleScript because the action controls an installed macOS application. OpenClip's JavaScriptCore runtime does not itself provide JXA's `Application()` interface.
- Requires Bob's Mac App Store edition (`com.hezongyidev.Bob`) and the normal first-use macOS permission for OpenClip to control Bob. No extra translation API key is required by the extension.
- Returns an empty string after the request so OpenClip does not paste the API response into the selected document.
- Provides a standard SF Symbol and English, Simplified Chinese, Traditional Chinese, French, and Japanese action metadata.

#### Privacy and licensing

The extension makes no direct network requests, collects no analytics, and does not read or write the clipboard. Selected text is sent to Bob locally via Apple Events; Bob may then send it to the translation providers the user has configured. This does not change Bob's own license or provider requirements.

The integration is independently implemented and MIT licensed. It does not copy the existing Bob–PopClip extension's code or bundle Bob's logo. The package README links to the independent source repository and issue tracker.

### Validation

- Tested on macOS with OpenClip **1.3.1** and Bob **1.20.0**. The working local prototype was installed by copying the package into the extension directory and enabling it in Actions; actual selection-to-translation behavior and the Automation prompt were confirmed manually.
- Version 1.0.0 retains the tested AppleScript behavior and adds the permanent identifier, localized metadata, license, and distribution documentation. The identifier migration is documented for users of the local prototype.
- The official `scripts/validate.sh` passes for the submitted package.
- Automated tests execute the production AppleScript JSON serializer without invoking Bob, covering Chinese, emoji, line breaks, carriage returns, tabs, quotes, backslashes, literal placeholders, and a 55,000-character input. The long-input check validates transport serialization, not translation-provider limits.
- The complete script was also invoked with fixed sample text and exited successfully with empty output.
- Only the four source package files are submitted under `raw/Bob.openclipext/`; generated `published/` assets are left to the catalog workflow.

### Author Checklist

- [x] Tested locally in OpenClip (manual folder installation and enablement, equivalent to the install helper; details above).
- [x] Validated manifest and scripts with `./scripts/validate.sh raw/Bob.openclipext`.
- [x] Uses a reverse-DNS identifier.
- [x] Declares version {{VERSION}}.
- [x] Uses a standard SF Symbol.
- [x] Does not use `openclip.pasteboard`; declares conservative `minOpenClipVersion: "1.3.1"`.

### Maintenance

The independent repository is the source of truth. Its release workflow submits the same versioned package through a PR to this catalog; upstream review remains required. It does not automatically merge changes or publish directly to the store. I am happy to adjust the package to the catalog's conventions.
