from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class Operation(Protocol):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...


class OperationFactory:
    def __init__(self):
        self._operations: dict[str, tuple[type[Operation], dict]] = {}
    
    def register(self, key: str, operation_class: type[Operation], dependencies: dict) -> None:
        if not issubclass(operation_class, Operation):
            raise ValueError(f"Operation {operation_class.__name__} must inherit from Operation")
        self._operations[key] = (operation_class, dependencies)
    
    def __getitem__(self, key: str) -> Operation:
        if key not in self._operations:
            raise KeyError(f"Operation {key} not registered")
        operation_class, dependencies = self._operations[key]
        return operation_class(**dependencies)