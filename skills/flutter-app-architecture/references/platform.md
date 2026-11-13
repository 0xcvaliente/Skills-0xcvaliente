# Platform details

## Localization (gen-l10n)

- `flutter pub add flutter_localizations --sdk=flutter` and `intl` (the SDK pins it, 0.20.x); `flutter: generate: true` in pubspec.
- `l10n.yaml`:
  ```yaml
  arb-dir: lib/l10n
  template-arb-file: app_en.arb
  output-localization-file: app_localizations.dart
  ```
- Import `l10n/app_localizations.dart`; `localizationsDelegates: AppLocalizations.localizationsDelegates`, `supportedLocales: AppLocalizations.supportedLocales`.
- **Norwegian:** name the file `app_nb.arb` (Bokmål). Devices can report `no`, `nb` or `nn`:
  ```dart
  localeResolutionCallback: (locale, supported) {
    final code = locale?.languageCode;
    if (code == 'no' || code == 'nn' || code == 'nb') return const Locale('nb');
    return supported.firstWhere((s) => s.languageCode == code, orElse: () => supported.first);
  },
  ```
  A server that uses `no` for Norwegian needs the app to send `no` when the app locale is `nb`.
- iOS: add `CFBundleLocalizations` (`en`, `nb`) to Info.plist so the App Store lists the languages.

## Info.plist keys

| Feature | Key |
|---|---|
| Photo library (image_picker) | `NSPhotoLibraryUsageDescription` |
| Camera | `NSCameraUsageDescription` |
| Face ID (local_auth) | `NSFaceIDUsageDescription` |
| Export compliance | `ITSAppUsesNonExemptEncryption` = false (HTTPS only) |
| Google sign-in | `GIDClientID`, `GIDServerClientID`, URL scheme = reversed client ID |
| Links checked with canLaunchUrl | `LSApplicationQueriesSchemes` |

Every string should say why, in the user's language (InfoPlist.strings per locale).

## Files and links

- `file_picker` 13.x (iOS 14+): `FilePicker.pickFiles()` returns `List<PlatformFile>` (empty on cancel); read with `readAsBytes()`. Older `FilePicker.platform.pickFiles` code breaks.
- `image_picker` 1.2.x uses PHPicker; downscale before upload (`maxWidth`, `imageQuality`).
- `url_launcher`: `launchUrl(uri, mode: LaunchMode.inAppBrowserView)` for web pages and hosted payment pages (SFSafariViewController), `externalApplication` for the browser.
- Authenticated PDFs: download with the API client, then open with a viewer or the share sheet; do not put the token in a URL.

## Push without Firebase on iOS

APNs directly: enable Push Notifications and Background Modes → Remote notifications, get the device token through a small platform channel, store it on the server (user, platform, token, locale), send with a `.p8` APNs key. `firebase_messaging` is the common cross-platform route but adds Google as a processor for iOS too. Keep personal data out of notification text.

## Reduce motion, contrast, transparency

`MediaQuery.disableAnimationsOf(context)` (reduce motion), `MediaQuery.highContrastOf(context)` (increase contrast). Flutter has no reduce-transparency flag; read `UIAccessibility.isReduceTransparencyEnabled` through a platform channel if glass must turn solid, and treat high contrast as reduce transparency meanwhile.
