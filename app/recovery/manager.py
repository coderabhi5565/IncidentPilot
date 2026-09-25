from app.recovery.strategy import (
    RecoveryStrategy,
    RetryStrategy,
    FallbackStrategy,
    ReplanStrategy,
)

class RecoveryManager:
    def __init__(self):
        self.strategies: dict[str, RecoveryStrategy] = {
            "retry": RetryStrategy(),
            "fallback": FallbackStrategy(),
            "replan": ReplanStrategy(),
        }

    def recover(
        self,
        tool_name: str,
        context: dict,
    ) -> dict:
        attempts = context.get("attempts", 0)

        if attempts == 0:
            strategy_name = "retry"
        elif attempts == 1:
            strategy_name = "fallback"
        else:
            strategy_name = "replan"

        strategy = self.strategies[strategy_name]

        result = strategy.execute(
            tool_name,
            context,
        )

        return result