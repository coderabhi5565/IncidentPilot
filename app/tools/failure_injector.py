class FailureInjector:
    def __init__(self):
        self.remaining_failures = {}

    def configure(self, failures: dict[str, int]) -> None:
        self.remaining_failures = failures.copy()

    def check(self, tool_name: str) -> None:
        remaining = self.remaining_failures.get(tool_name, 0)

        if remaining > 0:
            self.remaining_failures[tool_name] = remaining - 1

            raise RuntimeError(
                f"Injected failure for tool: {tool_name}"
            )


failure_injector = FailureInjector()