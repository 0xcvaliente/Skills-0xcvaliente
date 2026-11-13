---
name: flutter-app-architecture
description: "Structure, build and review production Flutter apps (Flutter 3.50+, Dart 3.14+) the way the official Flutter architecture guide recommends: UI and data layers, MVVM view models, repositories and services, Result and Command, dependency injection with provider or Riverpod 3, go_router with a tab shell and auth redirect, dio with token interceptors, secure token storage, gen-l10n localization (including Norwegian nb/no), deep links, file and image pickers, Google sign-in v7, and tests with fakes. Use when starting a Flutter app, adding a feature, connecting it to a REST backend, or reviewing Flutter code structure. Use flutter-ios-testflight to ship iOS builds, glassmorphism-liquid-glass for glass or Liquid Glass styling, and payload for the Payload CMS server side."
---

# Flutter app architecture

Follows docs.flutter.dev/app-architecture (the Compass reference app), checked 13 November 2026. Versions in [packages.md](references/packages.md); verify them with web search or `flutter pub add` before pinning.

## Shape of the app

```
lib/
  main.dart                     # build dependencies, runApp
  config/                       # environment: API base URL, flags (from --dart-define)
  routing/                      # router.dart (go_router), routes.dart (path constants)
  data/
    services/                   # one per external source: api_client.dart, token_store.dart
    repositories/<area>/        # abstract <x>_repository.dart + <x>_repository_remote.dart (+ _demo.dart)
  domain/models/                # immutable app models with fromJson
  ui/
    core/                       # theme, shared widgets (glass tab bar, empty/error/loading states)
    <feature>/view_models/      # <feature>_view_model.dart (ChangeNotifier + Commands)
    <feature>/widgets/          # <feature>_screen.dart and parts
  utils/                        # result.dart, command.dart
  l10n/                         # app_en.arb, app_nb.arb (+ generated)
test/                           # mirrors lib/; testing/fakes/ for fake repositories
```

`data/` is organised by type, `ui/` by feature. A domain layer (use cases) only when logic repeats across view models.

## Rules

1. **Layers.** Widgets render state and forward events. View models hold UI state and call repositories. Repositories are the source of truth (cache, map API JSON to models). Services wrap one external source and keep no state. No layer reaches past the next one down.
2. **Result, not exceptions, across layers.** Services and repositories return `Result<T>` (`Ok` / `Error`); view models `switch` on it exhaustively. See [patterns.md](references/patterns.md).
3. **Commands for user actions.** Each action a screen offers (load, apply, sign in) is a `Command` with `running`, `error`, `completed`; the widget listens with `ListenableBuilder`. Re-entry while running is ignored, which prevents double submits.
4. **Abstract repositories.** Define an abstract class per repository with a remote implementation and a fake/demo one. Pick the implementation in `main.dart` from config: the app then runs without a backend for demos and tests.
5. **Dependency injection** at the root (`MultiProvider`, or Riverpod providers). View models are created in the route builder, never as globals.
6. **Navigation** with go_router: `StatefulShellRoute.indexedStack` for bottom tabs (each tab keeps its stack), `redirect` + `refreshListenable` for the signed-in guard and role routing, `parentNavigatorKey: rootKey` for full-screen pages above the tab bar. See [navigation.md](references/navigation.md).
7. **Backend access** through one `ApiClient` (dio) with an interceptor that adds `Authorization: Bearer <token>` and turns 401 into "signed out". Never talk to a database directly from the app; never ship server secrets in the app. Tokens live in the iOS Keychain / Android Keystore (`flutter_secure_storage`), never in plain preferences. See [backend.md](references/backend.md).
8. **Server is the authority.** The app hides what a role cannot do for comfort, but every rule is enforced on the server. Treat every API response as untrusted input when parsing (null-safe `fromJson`, unknown enum values mapped to a fallback).
9. **Localization** with gen-l10n ARB files; no user-visible strings in widgets. Norwegian Bokmål is `nb`; map device locales `no`/`nn` to `nb`. See [platform.md](references/platform.md).
10. **Design packages.** Flutter 3.50 deprecates the in-SDK `material.dart`/`cupertino.dart` in favour of the `material_ui` and `cupertino_ui` packages (`dart fix --apply --code=migrate_design_widgets`). New apps start on the packages.
11. **Accessibility.** Semantics labels on icon-only controls, 44×44 pt targets, text scaling up to 200% without clipping, honour `MediaQuery.disableAnimationsOf` and `highContrastOf`.

## Workflow for a feature

1. Add or extend the model in `domain/models` from the real API response (copy field names exactly).
2. Add the method to the abstract repository, the remote implementation (service call + mapping) and the fake.
3. Write the view model with Commands; unit-test it against the fake repository.
4. Build the screen; widget-test the loading, error, empty and data states.
5. Register the route; check deep links and the back gesture.
6. Run `dart format --set-exit-if-changed .`, `flutter analyze`, `flutter test`. Report failures as they are.

## References

- [patterns.md](references/patterns.md): Result, Command, view model and screen templates.
- [navigation.md](references/navigation.md): go_router shell, auth redirect, universal links.
- [backend.md](references/backend.md): dio client, auth interceptor, token storage, uploads, Google sign-in v7, versioned API.
- [platform.md](references/platform.md): localization, Info.plist keys, pickers, url_launcher, push without Firebase.
- [packages.md](references/packages.md): versions verified November 2026.
- [testing.md](references/testing.md): fakes, widget and golden tests, CI commands.
- [sources.md](references/sources.md): where each fact comes from.
