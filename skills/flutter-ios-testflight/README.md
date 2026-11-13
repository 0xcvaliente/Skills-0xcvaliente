# Flutter to TestFlight

`flutter-ios-testflight` ships a Flutter app to Apple TestFlight, including from Linux or Windows with no Mac: the Apple account steps, signing made with openssl or by CI, a cloud macOS build on GitHub Actions or Codemagic, and the checks that make uploads fail.

Original work in this repository, researched 13 November 2026 (sources in [references/sources.md](references/sources.md)).

## Workflow

1. Prepare the app: bundle ID, icons, usage strings, export compliance, privacy manifest, build number.
2. Apple side (account holder): enrollment, App ID, App Store Connect record, API key.
3. Signing without a Mac: Codemagic, fastlane match, or openssl plus the portal.
4. Build and upload on a cloud Mac.
5. Add internal testers; prepare Beta App Review for external ones.

## Output

A working CI workflow and a checklist of the steps only the account holder can do.

## Related skills

- `flutter-app-architecture`: the app's code structure.
- `glassmorphism-liquid-glass`: iOS 26 glass styling.
