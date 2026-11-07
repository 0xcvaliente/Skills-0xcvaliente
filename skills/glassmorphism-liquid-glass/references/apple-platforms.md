# Apple platforms

API names below were checked against Apple's developer documentation in November 2026 (availability: iOS, iPadOS, Mac Catalyst and tvOS 26.0+, macOS 26.0+). Verify signatures against the SDK the project builds with.

## Contents

1. [Adoption order](#adoption-order)
2. [SwiftUI](#swiftui)
3. [UIKit](#uikit)
4. [AppKit](#appkit)
5. [Accessibility in custom views](#accessibility-in-custom-views)
6. [App icons](#app-icons)
7. [iOS 27 and the opt-out](#ios-27-and-the-opt-out)
8. [Testing](#testing)

## Adoption order

Work down this list and stop as soon as the design is met. Each step down adds code you must keep consistent with the system.

1. **Build with the current Xcode SDK.** Standard bars, sheets, popovers, menus and controls adopt Liquid Glass automatically.
2. **Remove custom backgrounds** from navigation and toolbars (`NavigationStack`, `NavigationSplitView`, `toolbar`, `UINavigationBar`, `UITabBar`, `UIToolbar`, `UISplitViewController`, `NSToolbar`, `NSSplitView`) and custom visual-effect views in sheets and popovers. They fight the system glass and the scroll edge effect.
3. **Use system styles** before custom effects: glass button styles, toolbar grouping, tab bar search role, sidebar-adaptable tabs.
4. **Custom glass only on the most important functional elements**, grouped in a container.
5. **Never put glass in the content layer** (lists, cards, backgrounds). Use `Material` (ultra-thin, thin, regular, thick) there if you need translucency.

Related system behaviour to adopt:

| Need | SwiftUI | UIKit | AppKit |
|---|---|---|---|
| Glass button | `.buttonStyle(.glass)`, `.glassProminent`, `.glass(_:)` | `UIButton.Configuration.glass()`, `.prominentGlass()`, `.clearGlass()`, `.prominentClearGlass()` | `NSButton.BezelStyle.glass` |
| Custom glass | `glassEffect(_:in:)` | `UIGlassEffect` in a `UIVisualEffectView` | `NSGlassEffectView` |
| Group and merge glass | `GlassEffectContainer(spacing:)` | `UIGlassContainerEffect` (`spacing`) | — |
| Scroll edge effect for a custom bar | `safeAreaBar(edge:alignment:spacing:content:)`, `scrollEdgeEffectStyle(_:for:)` | `UIScrollEdgeElementContainerInteraction` | — |
| Content extends under sidebar | `backgroundExtensionEffect()` | `UIBackgroundExtensionView` | `NSBackgroundExtensionView` |
| Concentric corners | `ConcentricRectangle`, `.rect(corners:isUniform:)` | `UIView.cornerConfiguration`, `UICornerConfiguration` | — |
| Tab bar shrinks on scroll | `.tabBarMinimizeBehavior(.onScrollDown)` | `tabBarMinimizeBehavior = .onScrollDown` | — |
| Search tab | `Tab(role: .search)` | `UISearchTab` | — |
| Tab bar becomes sidebar | `.tabViewStyle(.sidebarAdaptable)` | `UITabBarController.Mode.tabSidebar` | — |
| Split toolbar groups | `ToolbarSpacer(.fixed)` | `UIBarButtonItem.fixedSpace(_:)` | `NSToolbarItem.Identifier.space` |

## SwiftUI

**Basics.** `glassEffect` defaults to the regular variant in a capsule behind the view. Apply it after other modifiers that affect appearance.

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()

Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(in: .rect(cornerRadius: 16.0))

Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.tint(.orange).interactive())
```

**Containers, merging and morphing.** Put several glass views in one `GlassEffectContainer`: it renders them together (better performance) and lets shapes blend. Shapes closer than the container's `spacing` merge; larger spacing makes them merge sooner.

```swift
@State private var isExpanded = false
@Namespace private var namespace

var body: some View {
    GlassEffectContainer(spacing: 40.0) {
        HStack(spacing: 40.0) {
            Image(systemName: "scribble.variable")
                .frame(width: 80.0, height: 80.0)
                .font(.system(size: 36))
                .glassEffect()
                .glassEffectID("pencil", in: namespace)

            if isExpanded {
                Image(systemName: "eraser.fill")
                    .frame(width: 80.0, height: 80.0)
                    .font(.system(size: 36))
                    .glassEffect()
                    .glassEffectID("eraser", in: namespace)
            }
        }
    }

    Button("Toggle") {
        withAnimation { isExpanded.toggle() }
    }
    .buttonStyle(.glass)
}
```

- `glassEffectUnion(id:namespace:)` joins several views into one glass shape even at rest (useful for dynamically created views or views outside one stack).
- `glassEffectTransition(_:)`: `.matchedGeometry` (default for shapes within the container spacing) or `.materialize` (for shapes farther apart). Apple asks apps to use these two consistently; both do more than an opacity change.

**Clear glass over media, with dimming.** Clear has no adaptive behaviour, so add a dimming layer over bright media (Apple suggests about 35 % black), locally where the controls sit.

```swift
mediaView
    .overlay(alignment: .bottom) {
        LinearGradient(colors: [.clear, .black.opacity(0.35)], startPoint: .top, endPoint: .bottom)
            .frame(height: 160)
            .allowsHitTesting(false)
    }
    .overlay(alignment: .bottom) {
        PlaybackControls()          // bold, bright symbols
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .glassEffect(.clear.interactive(), in: .capsule)
            .padding(.bottom, 24)
    }
```

Skip the dimming over dark media or when using system AVKit playback controls, which dim on their own.

**Supporting earlier OS versions.**

```swift
extension View {
    @ViewBuilder
    func glassOrMaterial<S: Shape>(in shape: S) -> some View {
        if #available(iOS 26, macOS 26, tvOS 26, watchOS 26, *) {
            self.glassEffect(.regular, in: shape)
        } else {
            self.background(.ultraThinMaterial, in: shape)
        }
    }
}
```

**Performance.** Too many containers, or many effects outside containers, degrade performance. Limit the glass on screen at once and profile with Instruments.

## UIKit

```swift
let glass = UIGlassEffect(style: .regular)
glass.tintColor = .systemBlue        // only for the primary action
glass.isInteractive = true           // reacts to touch like system glass buttons

let glassView = UIVisualEffectView(effect: glass)
glassView.contentView.addSubview(iconView)

// Several glass elements rendered and merged together
let containerEffect = UIGlassContainerEffect()
containerEffect.spacing = 20         // distance at which elements begin to merge
let container = UIVisualEffectView(effect: containerEffect)
container.contentView.addSubview(glassView)
container.contentView.addSubview(otherGlassView)
```

- Shape: use `UIView.cornerConfiguration` with a `UICornerConfiguration` for capsule or container-concentric corners instead of hard-coded radii.
- Buttons: prefer `UIButton.Configuration.glass()` and `.prominentGlass()` (or the clear variants over media) over hand-built glass.
- Custom bars with content scrolling under them: add `UIScrollEdgeElementContainerInteraction` so they get the scroll edge effect.

## AppKit

`NSGlassEffectView` embeds its `contentView` in glass. Properties: `contentView`, `cornerRadius`, `effectIsInteractive`, `style`, `tintColor`. Buttons: `NSButton.BezelStyle.glass`. Toolbars and split views adopt glass automatically; remove custom backgrounds there.

## Accessibility in custom views

System glass adapts on its own to Reduce Transparency, Increase Contrast, Reduce Motion and the user's Liquid Glass look setting. Anything you draw yourself around it (gradients, dimming layers, shadows, custom blur) must adapt manually.

```swift
@Environment(\.accessibilityReduceTransparency) private var reduceTransparency
@Environment(\.accessibilityReduceMotion) private var reduceMotion
@Environment(\.colorSchemeContrast) private var contrast   // .increased when Increase Contrast is on
```

UIKit equivalents: `UIAccessibility.isReduceTransparencyEnabled`, `isReduceMotionEnabled`, `isDarkerSystemColorsEnabled`, with their change notifications.

- Custom colours on controls need light, dark and increased-contrast variants.
- Every icon-only control needs an accessibility label.
- Do not hide toolbar item content while leaving an empty item; hide the item itself.

## App icons

- Icons are built from layers; the system adds reflection, refraction, shadow, blur and highlights. Do not bake those effects into the artwork.
- Prefer simple, solid, overlapping semi-transparent shapes. Compose and preview in Icon Composer.
- Provide for the default (light), dark, clear and tinted appearances.
- iOS 27 lights only some icon elements and adds a layered depth effect; preview icons on the current OS.

## iOS 27 and the opt-out

- Apple's `UIDesignRequiresCompatibility` Info.plist key keeps the pre-Liquid Glass look and was always described as temporary.
- Per an Apple engineer on the developer forums (thread 832543, 2026): apps **linked against the iOS 26 SDK** still have the key honoured on iOS 27 devices; apps **linked against the iOS 27 SDK** have it ignored.
- Since 28 April 2026, App Store uploads must be built with Xcode 26 and the iOS 26 SDK. No date for requiring the iOS 27 SDK had been announced at the time of writing; check before planning around it.
- Plan for Liquid Glass, not for the opt-out. The `isLiquidGlassAvailable()` check in Expo (see [other-platforms.md](other-platforms.md)) reads this key too.

## Testing

- Toggle Reduce Transparency, Increase Contrast and Reduce Motion (device Settings, or the environment overrides in Xcode while debugging), dark mode, and the Liquid Glass look setting across its full range on iOS 27.
- Scroll real content under every bar: white pages, black pages, photos, text.
- Check rounded sheet corners and inset half sheets for clipped content.
- Profile scrolling and transitions with Instruments on the oldest supported device. Apple TV 4K (2nd generation) and newer render Liquid Glass; older Apple TV models keep the previous look.
