# mypy: ignore-errors

"""
Strategy pattern implementation example with regman.
"""

from abc import ABC, abstractmethod
from typing import Any

from regman import Registry, register


class PaymentStrategy(ABC):
    """Interface for payment strategies."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Processes a payment."""
        pass

    @abstractmethod
    def get_fee(self, amount: float) -> float:
        """Calculates transaction fees."""
        pass


class CreditCardStrategy(PaymentStrategy):
    """Credit card payment strategy."""

    def pay(self, amount: float) -> str:
        return f"Payment of ${amount:.2f} processed by credit card"

    def get_fee(self, amount: float) -> float:
        return amount * 0.03  # 3% fee


class PayPalStrategy(PaymentStrategy):
    """PayPal payment strategy."""

    def pay(self, amount: float) -> str:
        return f"Payment of ${amount:.2f} processed via PayPal"

    def get_fee(self, amount: float) -> float:
        return amount * 0.029 + 0.30  # 2.9% + 30¢


class BankTransferStrategy(PaymentStrategy):
    """Bank transfer payment strategy."""

    def pay(self, amount: float) -> str:
        return f"Payment of ${amount:.2f} processed by bank transfer"

    def get_fee(self, amount: float) -> float:
        return 0.0  # No fees


class CryptocurrencyStrategy(PaymentStrategy):
    """Cryptocurrency payment strategy."""

    def pay(self, amount: float) -> str:
        return f"Payment of ${amount:.2f} processed in cryptocurrency"

    def get_fee(self, amount: float) -> float:
        return amount * 0.01  # 1% fee


class PaymentProcessor:
    """Payment processor using the Strategy pattern."""

    def __init__(self) -> None:
        self.registry = Registry("payment_strategies")
        self._register_strategies()
        self.current_strategy = None

    def _register_strategies(self) -> None:
        """Registers all payment strategies."""

        @register(self.registry, "credit_card")
        class CreditCardPayment(CreditCardStrategy):
            pass

        @register(self.registry, "paypal")
        class PayPalPayment(PayPalStrategy):
            pass

        @register(self.registry, "bank_transfer")
        class BankTransferPayment(BankTransferStrategy):
            pass

        @register(self.registry, "crypto")
        class CryptoPayment(CryptocurrencyStrategy):
            pass

    def set_strategy(self, strategy_name: str) -> None:
        """Sets the payment strategy to use."""
        if strategy_name not in self.registry:
            raise ValueError(f"Strategy '{strategy_name}' not available")

        strategy_class = self.registry.get(strategy_name)
        self.current_strategy = strategy_class()

    def process_payment(self, amount: float) -> str:
        """Processes a payment with the current strategy."""
        if self.current_strategy is None:
            raise ValueError("No payment strategy selected")

        return self.current_strategy.pay(amount)

    def calculate_fee(self, amount: float) -> float:
        """Calculates fees with the current strategy."""
        if self.current_strategy is None:
            raise ValueError("No payment strategy selected")

        return self.current_strategy.get_fee(amount)

    def get_available_strategies(self) -> list[str]:
        """Returns the list of available strategies."""
        return self.registry.keys()

    def get_strategy_info(self, strategy_name: str) -> dict[str, Any]:
        """Returns information about a strategy."""
        if strategy_name not in self.registry:
            raise ValueError(f"Strategy '{strategy_name}' not available")

        strategy_class = self.registry.get(strategy_name)
        strategy = strategy_class()

        # Test with $100 amount to calculate fees
        test_amount = 100.0
        fee = strategy.get_fee(test_amount)

        return {
            "name": strategy_name,
            "fee_rate": fee / test_amount if test_amount > 0 else 0,
            "fixed_fee": (
                fee - (fee / test_amount * test_amount) if test_amount > 0 else 0
            ),
        }


def main() -> None:
    """Strategy pattern usage example."""
    print("=== Strategy pattern with regman ===\n")

    # Creating the payment processor
    processor = PaymentProcessor()

    # Displaying available strategies
    print("1. Available payment strategies:")
    for strategy_name in processor.get_available_strategies():
        info = processor.get_strategy_info(strategy_name)
        print(
            f"   - {strategy_name}: {info['fee_rate']:.1%} + ${info['fixed_fee']:.2f}"
        )
    print()

    # Test with different strategies
    amount = 1000.0
    print(f"2. Payment test of ${amount:.2f} with different strategies:")
    print()

    for strategy_name in processor.get_available_strategies():
        processor.set_strategy(strategy_name)
        fee = processor.calculate_fee(amount)
        total = amount + fee

        print(f"   {strategy_name.upper()}:")
        print(f"     {processor.process_payment(amount)}")
        print(f"     Fee: ${fee:.2f}")
        print(f"     Total: ${total:.2f}")
        print()

    # Payment process simulation
    print("3. Payment process simulation:")
    print()

    # User chooses PayPal
    chosen_strategy = "paypal"
    processor.set_strategy(chosen_strategy)

    print(f"   Selected strategy: {chosen_strategy}")
    print(f"   Amount: ${amount:.2f}")

    fee = processor.calculate_fee(amount)
    total = amount + fee

    print(f"   Fee: ${fee:.2f}")
    print(f"   Total: ${total:.2f}")
    print(f"   Result: {processor.process_payment(amount)}")
    print()

    # Cost comparison
    print("4. Cost comparison for different amounts:")
    print()

    amounts = [10.0, 100.0, 1000.0, 10000.0]

    print("   Amount | Card  | PayPal | Transfer | Crypto")
    print("   -------|-------|--------|----------|-------")

    for amount in amounts:
        costs = []
        for strategy_name in processor.get_available_strategies():
            processor.set_strategy(strategy_name)
            fee = processor.calculate_fee(amount)
            costs.append(f"${fee:.2f}")

        print(
            f"   ${amount:7.0f} | {costs[0]:5s} | {costs[1]:6s} | {costs[2]:8s} | {costs[3]:5s}"
        )


if __name__ == "__main__":
    main()
