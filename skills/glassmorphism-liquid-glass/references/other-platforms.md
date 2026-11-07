# Other platforms

The same rules apply everywhere: glass only on floating functional surfaces, a guaranteed-contrast fill, and a solid fallback for accessibility settings and weak hardware. Check package versions against the project before using these APIs.

## React Native and Expo

**`expo-glass-effect`** wraps the native iOS 26+ glass (Expo docs, SDK 54-58).

| Export | Use |
|---|---|
| `GlassView` | Props: `glassEffectStyle` (`'regular'` default, `'clear'`, `'none'`, or a config object with `style`, `animate`, `animationDuration`), `tintColor`, `isInteractive`, `colorScheme` (`'auto'`, `'light'`, `'dark'`), plus `View` props |
| `GlassContainer` | `spacing`: the distance at which child glass views start to merge |
| `isLiquidGlassAvailable()` | Whether the app can render Liquid Glass (system and compiler version, `UIDesignRequiresCompatibility`). It does not tell you whether the user reduced transparency. |
| `isGlassEffectAPIAvailable()` | Runtime check; some iOS 26 betas lack the API and `GlassView` can crash there. |

Caveats from the Expo docs:
- iOS and tvOS only. Elsewhere `GlassView` renders as a plain `View`, so style a real fallback (for example a `BlurView` from `expo-blur`, or a solid surface) instead of relying on the glass.
- Do not set `opacity` below 1 on a `GlassView` or its parents; at low opacity the glass stops rendering. To fade it, animate a wrapper's opacity and switch `glassEffectStyle` between your style and `'none'`.
- Check `AccessibilityInfo.isReduceTransparencyEnabled()` and switch to a solid surface yourself where you draw custom chrome.

```jsx
import { GlassView, isLiquidGlassAvailable } from 'expo-glass-effect';
import { View } from 'react-native';

const Bar = isLiquidGlassAvailable() ? GlassView : View;

<Bar
  style={[styles.bar, !isLiquidGlassAvailable() && styles.solidBar]}
  glassEffectStyle="regular"
  isInteractive
/>
```

For motion, sheets and gestures, use the animate-expo skill.

## Android and Jetpack Compose

- Material Design (including Material 3 Expressive) does not use glass. Translucent chrome on Android is a brand choice; keep it to bars and sheets and follow platform conventions elsewhere.
- Android 12 (API 31) added `RenderEffect.createBlurEffect`, which blurs a view's **own** content, and window-level background blur (`Window.setBackgroundBlurRadius`, `blurBehindRadius`). Devices and power-saving modes can disable cross-window blur (`WindowManager.isCrossWindowBlurEnabled`); provide a scrim fallback.
- Compose `Modifier.blur` also blurs the composable itself, not what is behind it. For backdrop blur use a library such as Haze (`chrisbanes/haze`, Compose Multiplatform). Its v2 API split into modules (`haze`, `haze-blur`, `haze-glass`); read the current docs before writing code.
- Test on a low-end device: blur is GPU-bound and older hardware may drop frames or skip the effect.

## Flutter

```dart
ClipRRect(                         // clip, or the blur covers everything behind the widget's bounds and beyond
  borderRadius: BorderRadius.circular(24),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
    child: Container(color: Colors.white.withValues(alpha: 0.55), child: content),
  ),
)
```

- Flutter 3.29 added `BackdropGroup` and `BackdropFilter.grouped`, which share one backdrop sample across many filters. Use them when several blurred widgets are visible at once.
- Read `MediaQuery.highContrastOf(context)` and the platform's reduce-transparency setting through your own platform channel or package if you need it, and swap in solid colours.

## Windows (Fluent)

Fluent's materials map cleanly onto the same layering idea:

- **Mica**: an opaque material tinted by the desktop wallpaper, sampled once. Use it for long-lived base surfaces such as the app background and title bar. Cheap. **Mica Alt** is a stronger tint for tabbed title bars.
- **Acrylic**: semi-transparent blur with tint, luminosity and noise. Use it for transient, light-dismiss surfaces such as flyouts and context menus. *Background acrylic* shows the desktop; *in-app acrylic* shows the app's own content.
- Both fall back to a solid colour when transparency effects are turned off, in battery saver, or on hardware that cannot render them. Design that solid state as carefully as the translucent one.

## visionOS

Windows use a system *glass* material that the app cannot modify. It adapts to the room and to virtual content, and visionOS has no separate dark mode. Prefer translucency to opaque window backgrounds; use `thin` material to mark interactive elements, `regular` to separate sections, and `thick` for dark elements on a regular background. Text uses the vibrancy hierarchy (label, secondary, tertiary).
