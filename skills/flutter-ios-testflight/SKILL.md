---
name: flutter-ios-testflight
description: "Ship a Flutter app to Apple TestFlight, including from a Linux or Windows machine with no Mac: Apple Developer enrollment, bundle ID and App Store Connect record, API keys, distribution certificates made with openssl or by CI, cloud macOS builds on GitHub Actions or Codemagic, build numbers, export compliance, privacy manifests, and internal versus external testers. Use when the user wants an iOS build of a Flutter app on TestFlight or the App Store, asks how to sign or upload without a Mac, or a TestFlight upload fails. Use flutter-app-architecture for the app's own code structure and glassmorphism-liquid-glass for iOS glass styling."
---

# Flutter to TestFlight

The upload needs Xcode, so it runs on a Mac. That Mac can be rented in the cloud: everything else (Apple account, certificate, profile, configuration) works from Linux in a browser and a shell. Verified November 2026; re-check versions and prices with web search before relying on them.

## Facts that decide the plan

- **Toolchain:** since 28 April 2026 uploads must be built with Xcode 26+ and the iOS 26 SDK. Apps must target iOS 13 or later (Flutter 3.50 templates default to 15.0).
- **Account:** Apple Developer Program, 99 USD a year. An *organization* account needs a D-U-N-S number and a legal entity; an *individual* account needs only a 2FA Apple Account but publishes under the person's name.
- **Testers:** internal (up to 100 people with a role in the team, no review, available minutes after processing) or external (up to 10,000, first build of a version goes through Beta App Review).
- **Swift Package Manager** is Flutter's default since 3.44; plugins without SwiftPM support fall back to CocoaPods, whose registry becomes read-only on 2 December 2026. Prefer plugins that support SwiftPM.

## Workflow

1. **Prepare the app** (any OS):
   - Unique `PRODUCT_BUNDLE_IDENTIFIER` in `ios/Runner.xcodeproj/project.pbxproj` (e.g. `com.company.app`).
   - `CFBundleDisplayName`, full icon set without transparency (generate with `flutter_launcher_icons`), launch screen.
   - `ITSAppUsesNonExemptEncryption = false` in `ios/Runner/Info.plist` when the app only uses HTTPS and OS crypto; otherwise every build waits in "Missing Compliance".
   - An `NS…UsageDescription` string for every permission the app or a plugin uses (photos, camera, Face ID, …).
   - `ios/Runner/PrivacyInfo.xcprivacy` when your code uses required-reason APIs; keep plugins current so their manifests are present.
   - Version `x.y.z+N` in `pubspec.yaml`; `N` is the build number and must go up on every upload (CI overrides it with `--build-number`).
2. **Apple side** (browser, account holder or admin): enroll; register an explicit App ID for the bundle ID; create the app record in App Store Connect; create a team API key (Users and Access → Integrations) and keep the Issuer ID, Key ID and the `.p8` (downloadable once). App Manager can upload; creating certificates through the API may need Admin.
3. **Signing without a Mac**, pick one ([signing.md](references/signing.md)):
   - Codemagic generates the distribution certificate and profile from the API key (least work).
   - fastlane `match` on the CI Mac, with the API key and an encrypted certificates repo.
   - openssl on Linux: make a CSR, upload it in the portal, convert the `.cer` to `.p12`, download the App Store profile, store both base64-encoded as CI secrets.
4. **Build in the cloud** ([ci.md](references/ci.md)): GitHub Actions `macos-26` runner (about 0.062 USD per minute; Free plan's 12 USD credit ≈ 190 macOS minutes a month) or Codemagic (500 free macOS minutes a month for a personal account; Estonian company, build machines in the US). Build with `flutter build ipa --release --build-number=<n> --export-options-plist=<file>`.
5. **Upload:** `xcrun altool --upload-app --type ios -f build/ios/ipa/*.ipa --apiKey <id> --apiIssuer <issuer>` (key file in `~/.appstoreconnect/private_keys/AuthKey_<id>.p8`), fastlane `upload_to_testflight`, or Codemagic's `publishing.app_store_connect`.
6. **TestFlight:** wait 5-30 minutes for processing; answer export compliance if asked; add internal testers. For external testers fill in the beta description, feedback email and review notes (include a demo account) and submit for Beta App Review.

## Rules

- Never commit the `.p8`, `.p12`, profile, or their passwords. Store them as CI secrets; delete the temporary keychain at the end of the job.
- Do not create a new distribution certificate on every run: Apple caps how many a team may have. Reuse one (match, Codemagic, or the stored `.p12`).
- Say plainly which steps need the account holder (enrollment, API key with the needed role, agreements in App Store Connect) and stop there: an agent cannot do them.
- The backend the TestFlight build talks to must be reachable from a tester's phone over HTTPS with a public certificate. A server reachable only on a private network (VPN, tailnet) needs that VPN on the phone.

## Troubleshooting

[troubleshooting.md](references/troubleshooting.md): missing compliance, ITMS-90xxx/91xxx upload errors, duplicate build numbers, profile/bundle mismatch, bitcode, icons with alpha.
- [sources.md](references/sources.md): where each fact comes from.
