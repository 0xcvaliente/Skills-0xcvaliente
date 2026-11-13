# Talking to a backend

## Principles

- The app talks to your server over HTTPS, never to the database. Anything in the app binary (keys, URLs, flags) is public.
- Prefer a small **versioned app API** (`/api/app/v1/...`) that returns screen-shaped JSON and calls the same server functions the website uses, over driving a CMS's generic collection API from the phone. Old app versions stay installed for months: keep v1 working, add v2 for breaking changes, and expose `GET /meta` with the lowest supported app version so an outdated app can ask for an update.
- Errors as JSON with a stable code (`{"error": "invalid_credentials"}`); map codes to localized messages in the app.

## dio client and auth interceptor

```dart
class ApiClient {
  ApiClient({required String baseUrl, required TokenStore tokens, required void Function() onUnauthorized})
      : _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 20),
          headers: {'Accept': 'application/json'},
        )) {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await tokens.read();
        if (token != null) options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
      onError: (e, handler) {
        if (e.response?.statusCode == 401) onUnauthorized();
        handler.next(e);
      },
    ));
  }

  final Dio _dio;

  Future<Result<Map<String, dynamic>>> getJson(String path, {Map<String, dynamic>? query}) async {
    try {
      final r = await _dio.get<Map<String, dynamic>>(path, queryParameters: query);
      return Result.ok(r.data ?? const {});
    } on DioException catch (e) {
      return Result.error(ApiException.from(e));
    }
  }
}
```

- With refresh tokens, use a `QueuedInterceptor` so only one refresh runs at a time, refresh with a separate `Dio` without the interceptor, mark the retried request (`extra['retried'] = true`) so it is retried once.
- Never log request headers or bodies that may hold tokens or personal data, in debug builds included.
- Uploads: `FormData.fromMap({'file': await MultipartFile.fromFile(path, filename: name)})`; build a new `FormData` for each attempt.

## Token storage

```dart
class TokenStore {
  static const _key = 'session_token';
  final _storage = const FlutterSecureStorage(
    iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock_this_device),
  );
  Future<String?> read() => _storage.read(key: _key);
  Future<void> write(String token) => _storage.write(key: _key, value: token);
  Future<void> clear() => _storage.delete(key: _key);
}
```

- `first_unlock_this_device`: available after the first unlock (background refresh works), not copied to backups or other devices.
- iOS Keychain items survive uninstall. On first launch after install (flag in `shared_preferences`), clear the stored token.
- Sign-out: call the server's logout (ends the session server-side), then clear the token, even if the call fails.

## Google sign-in (google_sign_in 7.x)

- `GoogleSignIn.instance.initialize(clientId: iosClientId, serverClientId: webClientId)` once; `authenticate()` on the button; listen to `authenticationEvents`.
- Send `account.authentication.idToken` to the server; the server verifies signature, `aud` (the web client ID), `iss`, expiry and `email_verified`, then starts its own session and returns the app token.
- Info.plist: `GIDClientID`, `GIDServerClientID`, and the reversed client ID in `CFBundleURLSchemes`.
- App Store guideline 4.8: offering Google sign-in may require Sign in with Apple as well; plan for it before review.

## Payload CMS backends

Payload 3 accepts `Authorization: Bearer <token>` (and `JWT <token>`) as well as its cookie. Its login returns `{ token, exp, user }`. Access functions apply to REST, GraphQL and the Local API, so a token gives the app exactly the rights the user has on the website. The `payload` skill covers the server side.
