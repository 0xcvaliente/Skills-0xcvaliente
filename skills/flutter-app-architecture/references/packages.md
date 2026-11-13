# Packages (verified on pub.dev, 13 November 2026)

Re-check before pinning: `flutter pub add <name>` resolves the newest compatible version.

| Need | Package | Version | Note |
|---|---|---|---|
| SDK | Flutter / Dart | 3.50.0 / 3.14 | iOS 15-27 supported; Xcode 26+ required for uploads |
| Design widgets | material_ui / cupertino_ui | 1.11.0 / 1.1.6 | Replace the deprecated in-SDK libraries |
| DI + view models | provider | 6.1.5+1 | Official guide's choice |
| Alternative DI/state | flutter_riverpod, riverpod_generator, riverpod_lint | 3.5.0, 4.0.10, 3.2.0 | Codegen through build_runner |
| Navigation | go_router | 18.1.4 | Needs Flutter ≥ 3.44 |
| HTTP | dio | 5.11.1 | Interceptors, multipart, cancel |
| JSON models | json_serializable / json_annotation | 6.15.2 / 4.12.0 | With build_runner 2.17.1 |
| Immutable models | freezed / freezed_annotation | 4.0.3 / 3.1.0 | |
| Secure storage | flutter_secure_storage | 11.2.0 | Keychain / Keystore |
| Biometrics | local_auth | 3.0.2 | `NSFaceIDUsageDescription` |
| Localization | flutter_localizations (SDK), intl | 0.20.x | gen-l10n |
| Google sign-in | google_sign_in | 7.2.0 | v7 API (`instance.initialize`, `authenticate`) |
| Files | file_picker | 13.3.3 | New owners; new API in 12/13 |
| Images | image_picker | 1.2.4 | PHPicker |
| Links | url_launcher | 6.3.3 | |
| Deep links (plugin) | app_links | 7.2.2 | Only if the built-in handling is not enough |
| Push | firebase_messaging | 17.0.1 | Or APNs directly |
| Mocks | mocktail | 1.0.5 | Prefer hand-written fakes |
| Lints | flutter_lints / very_good_analysis | 6.0.0 / 11.0.0 | |
| Glass | liquid_glass_widgets | 1.17.x | See glassmorphism-liquid-glass |

Prefer plugins that support Swift Package Manager (Flutter's iOS default since 3.44; the CocoaPods registry goes read-only on 2 December 2026).
