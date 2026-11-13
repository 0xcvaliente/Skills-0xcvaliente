# Signing an iOS build without a Mac

An App Store build needs one **Apple Distribution** certificate (with its private key) and one **App Store Connect** provisioning profile for the bundle ID.

## A. Let Codemagic create them

Add the App Store Connect API key as an integration, then in codemagic.yaml settings → Code signing identities → Generate certificate. Download the certificate when offered (only once) and keep it in a password manager. `ios_signing` in codemagic.yaml then fetches or creates the profile.

## B. fastlane match on the CI Mac

`match(type: "appstore", api_key_path: "...", git_url: "<private certs repo>")` creates or fetches the certificate and profile, encrypted with `MATCH_PASSWORD`, so every run reuses the same pair. Use `readonly: true` on CI after the first run.

## C. openssl on Linux plus the developer portal

```bash
openssl genrsa -out dist.key 2048
openssl req -new -key dist.key -out dist.csr \
  -subj "/emailAddress=you@example.com/CN=Your Name/C=NO"
# Portal → Certificates → + → Apple Distribution → upload dist.csr → download distribution.cer
openssl x509 -inform DER -in distribution.cer -out dist.pem
openssl pkcs12 -export -legacy -inkey dist.key -in dist.pem -out dist.p12
# Portal → Profiles → + → App Store Connect → pick the App ID and the certificate → download
base64 -w0 dist.p12 > dist.p12.b64
base64 -w0 App_AppStore.mobileprovision > profile.b64
```

`-legacy` keeps the `.p12` readable by macOS `security`, which may refuse OpenSSL 3's default encryption. Store the base64 files and the `.p12` password as CI secrets, then delete the local copies or keep them only in a password manager.

## Keys and roles

- API key role: App Manager is enough to upload. Creating certificates or profiles through the API, or cloud-managed signing, may need Admin.
- The `.p8` key downloads once. If lost, revoke it and create a new one.
- A distribution certificate lasts one year. Renewing it means new profiles too; the apps already on TestFlight keep working until their build expires (90 days).
