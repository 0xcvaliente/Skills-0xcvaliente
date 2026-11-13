# Flutter app architecture

`flutter-app-architecture` structures, builds and reviews production Flutter apps the way the official Flutter architecture guide (docs.flutter.dev/app-architecture) recommends, with the details a real app needs: a REST backend with session tokens, secure storage, navigation with a tab shell and role-based redirects, localization including Norwegian, and tests with fakes.

Original work in this repository, researched 13 November 2026 against Flutter 3.50 / Dart 3.14 and the current pub.dev packages, and used to build a production app (sources in [references/sources.md](references/sources.md)).

## Workflow

1. Lay out `lib/` by layer: services, repositories (abstract + remote + fake), models, view models, screens.
2. Pass `Result` between layers and expose user actions as `Command`s.
3. Wire dependencies at the root; build the router once, with a tab shell and an auth redirect.
4. Reach the backend only through one API client that adds the bearer token and maps errors to codes.
5. Keep every string in ARB files; parse JSON null-safely.
6. Test view models and screens against fakes; run format, analyze and test.

## Output

Code that follows the layers, plus tests; or a review listing where code crosses layers, holds secrets, logs personal data, or parses unsafely.

## Related skills

- `flutter-ios-testflight`: ship the iOS build.
- `glassmorphism-liquid-glass`: glass and Liquid Glass styling, including a tested Flutter tab bar.
- `payload`: the Payload CMS server side.
