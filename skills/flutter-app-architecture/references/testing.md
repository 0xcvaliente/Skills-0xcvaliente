# Testing

- **Fakes over mocks.** Put `FakeXRepository implements XRepository` in `testing/fakes/` with in-memory data and switches for failures. The same fake can power a demo mode of the app.
- **View model tests:** construct with fakes, run a command, assert state and `command.completed` / `command.error`.
- **Widget tests:** `testWidgets` + `pumpWidget(MaterialApp(localizationsDelegates: ..., home: Screen(viewModel: vm)))`; cover loading, error, empty and data; `await tester.pumpAndSettle()` after commands. Use `tester.binding.setSurfaceSize` for small phones and `MediaQuery(data: ...copyWith(textScaler: TextScaler.linear(2)))` for large text.
- **Router tests:** pump the real router with a fake auth state; assert redirects for signed out, each role, and deep links.
- **Golden tests:** `matchesGoldenFile`; generate them on one platform (CI) because fonts differ.
- **Integration tests:** `integration_test` (SDK) on a simulator or device; on Linux only Android emulators and desktop run.
- **CI:** `dart format --set-exit-if-changed .`, `flutter analyze`, `flutter test` on Linux (cheap); iOS builds only on macOS runners when shipping.
