# Result, Command, view model, screen

From docs.flutter.dev/app-architecture/design-patterns (result, command).

## Result

```dart
sealed class Result<T> {
  const Result();
  const factory Result.ok(T value) = Ok._;
  const factory Result.error(Exception error) = Error._;
}

final class Ok<T> extends Result<T> {
  const Ok._(this.value);
  final T value;
}

final class Error<T> extends Result<T> {
  const Error._(this.error);
  final Exception error;
}
```

Use: `switch (result) { case Ok(:final value): ...; case Error(:final error): ... }`. The `Error` name clashes with `dart:core`'s `Error`; that is what the official sample does, and it is fine inside your own files. Rename to `Failure` if it bothers you.

## Command

```dart
typedef CommandAction0<T> = Future<Result<T>> Function();
typedef CommandAction1<T, A> = Future<Result<T>> Function(A);

abstract class Command<T> extends ChangeNotifier {
  bool _running = false;
  bool get running => _running;
  Result<T>? _result;
  Result<T>? get result => _result;
  bool get error => _result is Error;
  bool get completed => _result is Ok;

  void clearResult() {
    _result = null;
    notifyListeners();
  }

  Future<void> _execute(CommandAction0<T> action) async {
    if (_running) return; // ignore double taps
    _running = true;
    _result = null;
    notifyListeners();
    try {
      _result = await action();
    } finally {
      _running = false;
      notifyListeners();
    }
  }
}

class Command0<T> extends Command<T> {
  Command0(this._action);
  final CommandAction0<T> _action;
  Future<void> execute() => _execute(_action);
}

class Command1<T, A> extends Command<T> {
  Command1(this._action);
  final CommandAction1<T, A> _action;
  Future<void> execute(A argument) => _execute(() => _action(argument));
}
```

## View model

```dart
class ProjectsViewModel extends ChangeNotifier {
  ProjectsViewModel({required ProjectRepository repository}) : _repository = repository {
    load = Command0(_load)..execute();
    apply = Command1(_apply);
  }

  final ProjectRepository _repository;
  late final Command0<void> load;
  late final Command1<void, int> apply;

  List<ProjectCard> _projects = const [];
  List<ProjectCard> get projects => _projects;

  Future<Result<void>> _load() async {
    final result = await _repository.list();
    if (result case Ok(:final value)) {
      _projects = value;
      notifyListeners();
    }
    return switch (result) { Ok() => const Result.ok(null), Error(:final error) => Result.error(error) };
  }

  Future<Result<void>> _apply(int id) => _repository.apply(id);
}
```

## Screen

```dart
class ProjectsScreen extends StatelessWidget {
  const ProjectsScreen({super.key, required this.viewModel});
  final ProjectsViewModel viewModel;

  @override
  Widget build(BuildContext context) => ListenableBuilder(
        listenable: Listenable.merge([viewModel, viewModel.load]),
        builder: (context, _) {
          if (viewModel.load.running && viewModel.projects.isEmpty) return const LoadingView();
          if (viewModel.load.error && viewModel.projects.isEmpty) {
            return ErrorView(onRetry: viewModel.load.execute);
          }
          return RefreshIndicator(
            onRefresh: viewModel.load.execute,
            child: ListView(children: [for (final p in viewModel.projects) ProjectTile(p)]),
          );
        },
      );
}
```

Show one-off results of an action (snackbar, navigation) by listening to the command in a `StatefulWidget` (`addListener` in `initState`, remove in `dispose`), then `clearResult()`.

## Models

Immutable classes with `final` fields and a `factory X.fromJson(Map<String, dynamic> json)`. For larger apps use `freezed` + `json_serializable` (build_runner). Map unknown enum strings to an `unknown` value instead of throwing: a newer server must not crash an older app.
