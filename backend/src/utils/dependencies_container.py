from typing import TypeVar, Callable

T = TypeVar("T")


class DependenciesContainer:
    dependencies: dict[type, Callable[[], T] | T] = {}

    def __setitem__(self, key: type[T], dependency: Callable[[], T] | T):
        self.dependencies[key] = dependency

    def __getitem__(self, key: type[T]) -> T:
        if key in self.dependencies:
            dependency = self.dependencies[key]
            return dependency() if callable(dependency) else dependency

        if isinstance(key, type):
            key = key.__name__

            if key not in self.dependencies:
                raise KeyError(f"Dependency for {key} is not set")

        elif isinstance(key, str):
            for cls_key in self.dependencies:
                if cls_key.__name__ == key:
                    key = cls_key
                    break
            else:
                raise KeyError(f"Dependency for {key} is not set")

        dependency = self.dependencies[key]
        return dependency() if callable(dependency) else dependency
