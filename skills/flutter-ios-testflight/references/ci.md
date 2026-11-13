# Cloud macOS builds

Researched 13 November 2026. Prices, runner labels and Xcode versions change; check them before use.

## GitHub Actions

- Runner `macos-26` (arm64, `macos-latest` points to it). Image 20261102 ships Xcode 26.6 (default) down to 26.0.1, fastlane 2.241.2, CocoaPods 1.17.0.
- Billing: free usage is a monthly dollar credit (Free 12 USD, Pro/Team 18 USD); macOS costs 0.062 USD/min, about 10× Linux. A Flutter iOS release build takes roughly 10-20 minutes.
- Public repositories build free; private ones spend the credit.

Workflow with a `.p12` and profile made on Linux ([signing.md](signing.md), option C). Secrets: `APPLE_TEAM_ID`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8_BASE64`, `DIST_P12_BASE64`, `DIST_P12_PASSWORD`, `APPSTORE_PROFILE_BASE64`, `KEYCHAIN_PASSWORD`.

```yaml
name: iOS TestFlight
on:
  workflow_dispatch:
  push:
    tags: ['v*']
jobs:
  ios:
    runs-on: macos-26
    timeout-minutes: 60
    env:
      BUNDLE_ID: com.example.app
      PROFILE_NAME: "Example AppStore"          # exact profile name in the portal
      TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
      ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
      ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
    steps:
      - uses: actions/checkout@v6
      - run: sudo xcode-select -s /Applications/Xcode_26.6.app
      - uses: subosito/flutter-action@v2
        with: { channel: stable, cache: true }

      - name: Install certificate and profile
        env:
          P12_BASE64: ${{ secrets.DIST_P12_BASE64 }}
          P12_PASSWORD: ${{ secrets.DIST_P12_PASSWORD }}
          PROFILE_BASE64: ${{ secrets.APPSTORE_PROFILE_BASE64 }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          KC="$RUNNER_TEMP/build.keychain-db"
          echo "$P12_BASE64" | base64 --decode > "$RUNNER_TEMP/dist.p12"
          security create-keychain -p "$KEYCHAIN_PASSWORD" "$KC"
          security set-keychain-settings -lut 21600 "$KC"
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KC"
          security import "$RUNNER_TEMP/dist.p12" -P "$P12_PASSWORD" -A -t cert -f pkcs12 -k "$KC"
          security set-key-partition-list -S apple-tool:,apple: -k "$KEYCHAIN_PASSWORD" "$KC"
          security list-keychain -d user -s "$KC"
          for d in "$HOME/Library/Developer/Xcode/UserData/Provisioning Profiles" \
                   "$HOME/Library/MobileDevice/Provisioning Profiles"; do
            mkdir -p "$d"; echo "$PROFILE_BASE64" | base64 --decode > "$d/appstore.mobileprovision"
          done

      - name: App Store Connect API key
        env: { ASC_KEY_P8_BASE64: '${{ secrets.ASC_KEY_P8_BASE64 }}' }
        run: |
          mkdir -p ~/.appstoreconnect/private_keys
          echo "$ASC_KEY_P8_BASE64" | base64 --decode > ~/.appstoreconnect/private_keys/AuthKey_${ASC_KEY_ID}.p8

      - name: Manual signing for Release
        run: |
          fastlane run update_code_signing_settings path:ios/Runner.xcodeproj \
            use_automatic_signing:false targets:Runner build_configurations:Release \
            team_id:"$TEAM_ID" code_sign_identity:"Apple Distribution" \
            profile_name:"$PROFILE_NAME" bundle_identifier:"$BUNDLE_ID"

      - name: ExportOptions.plist
        run: |
          cat > "$RUNNER_TEMP/ExportOptions.plist" <<EOF
          <?xml version="1.0" encoding="UTF-8"?>
          <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
          <plist version="1.0"><dict>
            <key>method</key><string>app-store-connect</string>
            <key>teamID</key><string>${TEAM_ID}</string>
            <key>signingStyle</key><string>manual</string>
            <key>signingCertificate</key><string>Apple Distribution</string>
            <key>provisioningProfiles</key><dict><key>${BUNDLE_ID}</key><string>${PROFILE_NAME}</string></dict>
            <key>uploadSymbols</key><true/>
          </dict></plist>
          EOF

      - name: Build IPA
        run: |
          flutter build ipa --release \
            --build-number=$((GITHUB_RUN_NUMBER + 100)) \
            --export-options-plist="$RUNNER_TEMP/ExportOptions.plist"

      - name: Upload to TestFlight
        run: |
          xcrun altool --upload-app --type ios -f build/ios/ipa/*.ipa \
            --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"

      - name: Remove keychain
        if: always()
        run: security delete-keychain "$RUNNER_TEMP/build.keychain-db" || true
```

Notes:
- If `fastlane run` rejects `targets:Runner`, commit the manual signing settings to `project.pbxproj` for the Release configuration instead.
- `altool --upload-app` is reported as deprecated in favour of `--upload-package` but still works; fastlane `upload_to_testflight` with `api_key_path` is the alternative.
- Build number: `run_number + offset` always increases. Alternatively read the latest with fastlane `latest_testflight_build_number` and add 1.

## Codemagic

- Free: 500 macOS M2 minutes a month (personal account), one concurrent build. Pay as you go: M2 0.095 USD/min.
- Company: Nevercode OÜ, Tartu, Estonia (owned by Nevercode Ltd, UK). Build machines run in the US.
- Add the API key under Team → Integrations → Developer Portal. Codemagic can generate the distribution certificate from it (download it once and keep it).

```yaml
workflows:
  ios-testflight:
    name: iOS TestFlight
    max_build_duration: 60
    instance_type: mac_mini_m2
    integrations:
      app_store_connect: AppStoreKey        # name given to the key in Codemagic
    environment:
      ios_signing:
        distribution_type: app_store
        bundle_identifier: com.example.app
      vars:
        APP_STORE_APPLE_ID: 1234567890      # numeric Apple ID of the app record
      flutter: stable
      xcode: latest
    triggering:
      events: [tag]
    scripts:
      - name: Signing profiles
        script: xcode-project use-profiles  # also writes /Users/builder/export_options.plist
      - name: Packages
        script: flutter pub get
      - name: Build IPA
        script: |
          BUILD_NUMBER=$(($(app-store-connect get-latest-app-store-build-number "$APP_STORE_APPLE_ID") + 1))
          flutter build ipa --release --build-number=$BUILD_NUMBER \
            --export-options-plist=/Users/builder/export_options.plist
    artifacts:
      - build/ios/ipa/*.ipa
      - /tmp/xcodebuild_logs/*.log
    publishing:
      app_store_connect:
        auth: integration
        submit_to_testflight: true
```

If a plugin still needs CocoaPods, add a step `find . -name Podfile -execdir pod install \;` before the build.

## Choosing

| | GitHub Actions | Codemagic |
|---|---|---|
| Setup work | More secrets, own signing steps | Least: signing generated from the API key |
| Free macOS minutes | About 190 (Free plan, private repo) | 500 |
| Code location | Same place as the repo | Separate service with repo access |
| Data location | GitHub (US) | Company EU, machines US |
