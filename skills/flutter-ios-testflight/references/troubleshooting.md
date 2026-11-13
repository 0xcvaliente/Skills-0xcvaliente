# TestFlight upload problems

| Symptom | Cause | Fix |
|---|---|---|
| Build shows "Missing Compliance" | No export compliance answer | `ITSAppUsesNonExemptEncryption` = `false` in Info.plist (HTTPS and OS crypto only), or answer in App Store Connect |
| "The bundle version must be higher than the previously uploaded version" | Build number reused | Pass a higher `--build-number`; derive it from the CI run number or the latest TestFlight build + 1 |
| "No profiles for 'x' were found" / profile doesn't match | Bundle ID in the project differs from the profile, or the profile was made for another certificate | Align `PRODUCT_BUNDLE_IDENTIFIER`, the App ID and the profile; regenerate the profile after a new certificate |
| Upload rejected for icon | Icon with transparency, or a missing size | Regenerate the icon set from a 1024×1024 PNG without alpha |
| ITMS-90683 missing purpose string | A plugin uses a protected API without its usage text | Add the `NS…UsageDescription` key named in the email |
| ITMS-91053 / privacy manifest warnings | Required-reason API without a declared reason, or outdated plugin | Update plugins; add `PrivacyInfo.xcprivacy` with the reasons for your own code |
| "Invalid SDK" or Xcode version error | Built with Xcode older than required | Select Xcode 26+ on the runner (`xcode-select`) |
| Bitcode errors | Old plugin sets `ENABLE_BITCODE` | Remove it; bitcode is gone since Xcode 14 |
| `security: SecKeychainItemImport: MAC verification failed` | `.p12` made with OpenSSL 3 defaults or wrong password | Re-export with `openssl pkcs12 -export -legacy`; check the secret |
| CocoaPods errors in CI | A plugin without SwiftPM support | Update the plugin, or run `pod install` before the build; the CocoaPods registry is read-only from 2 Dec 2026 |
| Testers can't reach the server | Server not public, or self-signed certificate | Use a public HTTPS address with a trusted certificate, or put the VPN app on the tester's phone |
