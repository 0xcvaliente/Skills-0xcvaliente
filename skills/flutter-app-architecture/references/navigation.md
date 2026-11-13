# Navigation with go_router (18.x)

## Tab shell plus auth redirect

```dart
final rootKey = GlobalKey<NavigatorState>();

GoRouter buildRouter(AuthState auth) => GoRouter(
      navigatorKey: rootKey,
      initialLocation: '/home',
      refreshListenable: auth, // notifies on sign-in, sign-out, role change
      redirect: (context, state) {
        final at = state.matchedLocation;
        if (!auth.signedIn) return at.startsWith('/sign-in') ? null : '/sign-in';
        if (at.startsWith('/sign-in')) return '/home';
        return null; // role-specific redirects go here too
      },
      routes: [
        GoRoute(path: '/sign-in', builder: (_, _) => const SignInScreen()),
        StatefulShellRoute.indexedStack(
          builder: (context, state, shell) => AppShell(shell: shell),
          branches: [
            StatefulShellBranch(routes: [
              GoRoute(path: '/home', builder: (_, _) => const HomeScreen(), routes: [
                GoRoute(
                  path: 'item/:id',
                  parentNavigatorKey: rootKey, // full screen, above the tab bar
                  builder: (_, s) => ItemScreen(id: int.parse(s.pathParameters['id']!)),
                ),
              ]),
            ]),
            StatefulShellBranch(routes: [GoRoute(path: '/settings', builder: (_, _) => const SettingsScreen())]),
          ],
        ),
      ],
    );
```

- `shell.goBranch(i, initialLocation: i == shell.currentIndex)`: re-tapping the active tab pops it to its root, as on iOS.
- Each branch keeps its own navigator, so tab state survives switching.
- Build the router once (not in `build`), or the app resets its location on every rebuild.
- Different tab sets per role: either one shell per role (`/s/...` for one role, `/c/...` for another) with a redirect choosing the shell, or one shell whose branches are built from the role. Separate shells keep routes and deep links simpler.

## iOS universal links

- Flutter ≥ 3.27 handles deep links by default. Set `FlutterDeepLinkingEnabled` to `NO` only when a plugin such as `app_links` handles them instead.
- Entitlement `com.apple.developer.associated-domains` = `applinks:example.com` in `ios/Runner/Runner.entitlements` (needs a paid team).
- Serve `https://example.com/.well-known/apple-app-site-association` (no extension, JSON):
  `{"applinks":{"details":[{"appIDs":["TEAMID.com.example.app"],"components":[{"/":"/en/magic/*"}]}]}}`
- Apple's CDN caches the file up to 24 hours. Test with `xcrun simctl openurl booted https://example.com/...`.
- Incoming paths go through `redirect`, so a signed-out user opening a deep link lands on sign-in first; keep the target in a `from` query parameter.
- Android App Links: `/.well-known/assetlinks.json` and an intent filter with `android:autoVerify="true"`.
