# Flutter: glass tab bar

Researched and built 13 November 2026 (Flutter 3.50, Dart 3.14). The widget below compiles, and its widget tests pass: the solid fallback under Increase Contrast and the selected-tab semantics. It ran in a shipping-bound app; re-check package versions before relying on them.

## State of Liquid Glass in Flutter

- **No native Liquid Glass yet.** flutter/flutter#170310 is open at P3. Cupertino work for iOS 26 happens in the standalone `cupertino_ui` package (early ports in flutter/packages #13162/#13163, unmerged). `CupertinoTabBar` still draws the pre-26 flat translucent bar.
- **Design libraries moved out of the SDK.** Flutter 3.50 deprecates `package:flutter/material.dart` and `cupertino.dart` in favour of `material_ui` and `cupertino_ui` (`dart fix --apply --code=migrate_design_widgets`). `CupertinoPageTransitionsBuilder` and `GlobalCupertinoLocalizations` come from `cupertino_ui`; `GlobalMaterialLocalizations` from `material_ui`. Mixing the SDK's deprecated delegates with the packages' widgets leaves them without their translations.
- **Flutter exposes no Reduce Transparency flag.** Use `MediaQuery.highContrastOf` as the trigger for the solid fallback, plus an explicit `reduceTransparency` parameter you can feed from a platform channel (`UIAccessibility.isReduceTransparencyEnabled`).

## Options

| Approach | Use when | Caveats |
|---|---|---|
| **Pure Flutter blur bar** (below) | Default. Any platform, Impeller or Skia | Frosted, no lensing |
| `liquid_glass_widgets` (MIT, 1.17.x) | You want refraction; has `GlassTabBar.bottom` and a blur fallback tier | Shader cost; first-launch quality benchmark is experimental; can't detect Reduce Transparency |
| `liquid_glass_renderer` (Apache-2.0, 1.0.0-dev) | Experiments only | Prerelease, needs Impeller and the Flutter GPU preview flag |
| `adaptive_platform_ui` (native `UITabBar` on iOS 26) | Pixel-exact system bar is a hard requirement | Platform views, iOS-only glass, awkward with go_router shells |
| `cupertino_native` | Avoid | Stale proof of concept |

## Pure Flutter recipe

- `Scaffold(extendBody: true, bottomNavigationBar: GlassTabBar(...))` so content scrolls under the bar; pad lists by the bar height plus `MediaQuery.viewPaddingOf(context).bottom`.
- Floating capsule: outer `Padding` (20 side, `max(viewPadding.bottom, 12)` bottom) → shadow with a negative `spreadRadius` (a plain shadow under a translucent capsule reads as a grey slab) → `ClipRRect` → `BackdropFilter(ImageFilter.blur(σ≈22))` → tint fill (surface at ~60 % alpha light, ~55 % dark) + top-light gradient + 0.6 px white rim.
- Selection pill: `AnimatedAlign` with `AlignmentDirectional` (RTL-safe), duration zero when `MediaQuery.disableAnimationsOf`.
- Haptics: `HapticFeedback.selectionClick()` only when the tab changes; re-tap pops the tab to its root (`shell.goBranch(i, initialLocation: i == shell.currentIndex)`).
- Semantics per tab: `button`, `selected`, `inMutuallyExclusiveGroup`, `label`; clamp label text scaling to 1.3× inside the bar.
- Several blurred surfaces on one screen: wrap them in `BackdropGroup` and use `BackdropFilter.grouped` to share one backdrop read.

```dart
import 'dart:math' as math;
import 'dart:ui' show ImageFilter;

import 'package:flutter/services.dart';
import 'package:material_ui/material_ui.dart';

class GlassTabItem {
  const GlassTabItem({required this.icon, required this.label, IconData? activeIcon})
    : activeIcon = activeIcon ?? icon;

  final IconData icon;
  final IconData activeIcon;
  final String label;
}

/// A floating capsule tab bar in the style of iOS 26 Liquid Glass.
///
/// Flutter has no Liquid Glass yet (flutter/flutter#170310), so this approximates it: a clipped
/// backdrop blur, a translucent tint, a top rim light and a sliding selection pill. Content
/// scrolls underneath (the Scaffold needs `extendBody: true`).
///
/// Accessibility: with Increase Contrast on (or [reduceTransparency]) the bar turns solid with a
/// stronger border, since Flutter exposes no Reduce Transparency flag. Reduce Motion stops the
/// pill animation. Labels scale with the text size up to 1.3x inside the bar.
class GlassTabBar extends StatelessWidget {
  const GlassTabBar({
    super.key,
    required this.items,
    required this.currentIndex,
    required this.onTap,
    this.reduceTransparency = false,
    this.blurSigma = 22,
  }) : assert(items.length >= 2);

  final List<GlassTabItem> items;
  final int currentIndex;
  final ValueChanged<int> onTap;
  final bool reduceTransparency;
  final double blurSigma;

  /// Height of the bar itself, without the safe-area margin.
  static const barHeight = 64.0;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final scheme = theme.colorScheme;
    final dark = theme.brightness == Brightness.dark;
    final highContrast = MediaQuery.highContrastOf(context);
    final solid = reduceTransparency || highContrast;
    final noMotion = MediaQuery.disableAnimationsOf(context);
    final bottom = math.max(MediaQuery.viewPaddingOf(context).bottom, 12.0);
    final scaler = MediaQuery.textScalerOf(context).clamp(minScaleFactor: 1.0, maxScaleFactor: 1.3);
    const radius = BorderRadius.all(Radius.circular(32));
    final count = items.length;

    final fill = solid
        ? scheme.surfaceContainerHighest
        : scheme.surface.withValues(alpha: dark ? 0.55 : 0.62);
    final rim = highContrast ? scheme.outline : Colors.white.withValues(alpha: dark ? 0.16 : 0.55);

    Widget bar = DecoratedBox(
      decoration: BoxDecoration(
        color: fill,
        borderRadius: radius,
        border: Border.all(color: rim, width: highContrast ? 1.5 : 0.6),
        gradient: solid
            ? null
            : LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.white.withValues(alpha: dark ? 0.10 : 0.35),
                  Colors.white.withValues(alpha: 0),
                ],
                stops: const [0, 0.55],
              ),
      ),
      child: SizedBox(
        height: barHeight,
        child: Padding(
          padding: const EdgeInsets.all(5),
          child: Stack(
            children: [
              Positioned.fill(
                child: AnimatedAlign(
                  alignment: AlignmentDirectional(-1 + 2 * currentIndex / (count - 1), 0),
                  duration: noMotion ? Duration.zero : const Duration(milliseconds: 340),
                  curve: Curves.easeOutBack,
                  child: FractionallySizedBox(
                    widthFactor: 1 / count,
                    heightFactor: 1,
                    child: DecoratedBox(
                      decoration: BoxDecoration(
                        color: scheme.primary.withValues(alpha: solid ? 0.22 : (dark ? 0.22 : 0.13)),
                        borderRadius: const BorderRadius.all(Radius.circular(27)),
                      ),
                    ),
                  ),
                ),
              ),
              Row(
                children: [
                  for (var i = 0; i < count; i++)
                    Expanded(
                      child: _Tab(
                        item: items[i],
                        selected: i == currentIndex,
                        scaler: scaler,
                        highContrast: highContrast,
                        onTap: () => _tap(i),
                      ),
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );

    if (!solid) {
      bar = BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blurSigma, sigmaY: blurSigma),
        child: bar,
      );
    }

    return Padding(
      padding: EdgeInsets.fromLTRB(20, 0, 20, bottom),
      child: DecoratedBox(
        decoration: BoxDecoration(
          borderRadius: radius,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: dark ? 0.35 : 0.08),
              blurRadius: 24,
              spreadRadius: -6,
              offset: const Offset(0, 8),
            ),
          ],
        ),
        child: ClipRRect(borderRadius: radius, child: bar),
      ),
    );
  }

  void _tap(int index) {
    if (index != currentIndex) HapticFeedback.selectionClick();
    onTap(index);
  }
}

class _Tab extends StatelessWidget {
  const _Tab({
    required this.item,
    required this.selected,
    required this.scaler,
    required this.highContrast,
    required this.onTap,
  });

  final GlassTabItem item;
  final bool selected;
  final TextScaler scaler;
  final bool highContrast;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final color = selected ? scheme.primary : scheme.onSurface.withValues(alpha: highContrast ? 1 : 0.68);
    return Semantics(
      button: true,
      selected: selected,
      inMutuallyExclusiveGroup: true,
      label: item.label,
      onTap: onTap,
      excludeSemantics: true,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedScale(
              scale: selected ? 1.08 : 1,
              duration: MediaQuery.disableAnimationsOf(context)
                  ? Duration.zero
                  : const Duration(milliseconds: 200),
              child: Icon(selected ? item.activeIcon : item.icon, color: color, size: 24),
            ),
            const SizedBox(height: 2),
            Text(
              item.label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textScaler: scaler,
              style: TextStyle(
                fontSize: 11,
                color: color,
                fontWeight: selected ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### go_router shell

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, shell) => Scaffold(
    extendBody: true,
    body: shell,
    bottomNavigationBar: GlassTabBar(
      items: const [
        GlassTabItem(icon: Icons.home_outlined, activeIcon: Icons.home_rounded, label: 'Home'),
        GlassTabItem(icon: Icons.person_outline_rounded, activeIcon: Icons.person_rounded, label: 'Profile'),
      ],
      currentIndex: shell.currentIndex,
      onTap: (i) => shell.goBranch(i, initialLocation: i == shell.currentIndex),
    ),
  ),
  branches: [/* one StatefulShellBranch per tab */],
)
```

Full-screen detail pages that should cover the bar use `parentNavigatorKey: rootNavigatorKey`.

### Test it

```dart
testWidgets('solid with Increase Contrast', (tester) async {
  Widget bar(bool hc) => MaterialApp(
        home: MediaQuery(
          data: MediaQueryData(highContrast: hc),
          child: Scaffold(
            bottomNavigationBar: GlassTabBar(
              items: const [GlassTabItem(icon: Icons.home, label: 'Home'), GlassTabItem(icon: Icons.person, label: 'Profile')],
              currentIndex: 1,
              onTap: (_) {},
            ),
          ),
        ),
      );
  await tester.pumpWidget(bar(false));
  expect(find.byType(BackdropFilter), findsOneWidget);
  await tester.pumpWidget(bar(true));
  expect(find.byType(BackdropFilter), findsNothing);
});
```

To look at the result on Linux without a phone, render goldens with real fonts: load Roboto through `FontLoader` under the families the theme asks for (`CupertinoSystemText`, `CupertinoSystemDisplay` on an iOS theme) and `MaterialIcons`, from `$FLUTTER_ROOT/bin/cache/artifacts/material_fonts`, then `matchesGoldenFile` with `--update-goldens` and view the PNGs. Check light, dark, a busy backdrop under the bar, and large text.
