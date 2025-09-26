# mypy: ignore-errors

"""
Observer pattern implementation example with regman.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime

from regman import Registry, register


class Observer(ABC):
    """Interface for observers."""

    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        """Updates the observer with an event."""
        pass


class LoggerObserver(Observer):
    """Observer that logs events to a log file."""

    def __init__(self) -> None:
        self.logs: List[Dict[str, Any]] = []

    def update(self, event: str, data: Any) -> None:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "data": data,
        }
        self.logs.append(log_entry)
        print(f"[LOG] {log_entry['timestamp']} - {event}: {data}")

    def get_logs(self) -> List[Dict[str, Any]]:
        """Returns all logs."""
        return self.logs.copy()

    def clear_logs(self) -> None:
        """Clears all logs."""
        self.logs.clear()


class EmailNotifier(Observer):
    """Observer that sends email notifications."""

    def __init__(self) -> None:
        self.emails: List[Dict[str, Any]] = []

    def update(self, event: str, data: Any) -> None:
        email = {
            "to": "admin@example.com",
            "subject": f"Notification: {event}",
            "body": f"Event '{event}' detected with data: {data}",
            "timestamp": datetime.now().isoformat(),
        }
        self.emails.append(email)
        print(f"[EMAIL] Sent to {email['to']}: {email['subject']}")

    def get_emails(self) -> List[Dict[str, Any]]:
        """Returns all sent emails."""
        return self.emails.copy()


class MetricsCollector(Observer):
    """Observer that collects metrics."""

    def __init__(self) -> None:
        self.metrics: Dict[str, int] = {}

    def update(self, event: str, data: Any) -> None:
        # Increment counter for this event
        self.metrics[event] = self.metrics.get(event, 0) + 1
        print(f"[METRICS] {event}: {self.metrics[event]} occurrences")

    def get_metrics(self) -> Dict[str, int]:
        """Returns all metrics."""
        return self.metrics.copy()

    def get_event_count(self, event: str) -> int:
        """Returns the number of occurrences of an event."""
        return self.metrics.get(event, 0)


class EventSubject:
    """Subject that notifies observers of events."""

    def __init__(self) -> None:
        self.observers: List[Observer] = []
        self.registry = Registry("observers")
        self._register_observers()

    def _register_observers(self) -> None:
        """Registers all observers."""

        @register(self.registry, "logger")
        class LoggerObserverClass(LoggerObserver):
            pass

        @register(self.registry, "email")
        class EmailNotifierClass(EmailNotifier):
            pass

        @register(self.registry, "metrics")
        class MetricsCollectorClass(MetricsCollector):
            pass

    def add_observer(self, observer_name: str) -> None:
        """Adds an observer by its name."""
        if observer_name not in self.registry:
            raise ValueError(f"Observer '{observer_name}' not available")

        observer_class = self.registry.get(observer_name)
        observer = observer_class()
        self.observers.append(observer)
        print(f"Observer '{observer_name}' added")

    def remove_observer(self, observer_name: str) -> None:
        """Removes an observer by its name."""
        # For simplicity, we remove the first observer of the given type
        for i, observer in enumerate(self.observers):
            if (
                observer.__class__.__name__.lower().replace("class", "")
                == observer_name.lower()
            ):
                del self.observers[i]
                print(f"Observer '{observer_name}' removed")
                return
        print(f"Observer '{observer_name}' not found")

    def notify_observers(self, event: str, data: Any) -> None:
        """Notifies all observers of an event."""
        print(f"\n--- Notification: {event} ---")
        for observer in self.observers:
            observer.update(event, data)
        print("--- End of notification ---\n")

    def get_available_observers(self) -> List[str]:
        """Returns the list of available observers."""
        return self.registry.keys()

    def get_observer_count(self) -> int:
        """Returns the number of active observers."""
        return len(self.observers)


def main() -> None:
    """Observer pattern usage example."""
    print("=== Observer pattern with regman ===\n")

    # Creating the subject
    subject = EventSubject()

    # Displaying available observers
    print("1. Available observers:")
    for observer_name in subject.get_available_observers():
        print(f"   - {observer_name}")
    print()

    # Adding observers
    print("2. Adding observers:")
    subject.add_observer("logger")
    subject.add_observer("email")
    subject.add_observer("metrics")
    print(f"   Number of active observers: {subject.get_observer_count()}")
    print()

    # Event simulation
    print("3. Event simulation:")

    # User login event
    subject.notify_observers(
        "user_login",
        {"user_id": 123, "username": "john_doe", "ip_address": "192.168.1.100"},
    )

    # Purchase event
    subject.notify_observers(
        "purchase",
        {"user_id": 123, "product_id": "PROD-001", "amount": 99.99, "currency": "USD"},
    )

    # Error event
    subject.notify_observers(
        "error",
        {
            "error_code": "E001",
            "message": "Database connection failed",
            "severity": "high",
        },
    )

    # User logout event
    subject.notify_observers(
        "user_logout", {"user_id": 123, "session_duration": 1800}  # 30 minutes
    )

    # Displaying metrics
    print("4. Collected metrics:")
    metrics_observer = subject.observers[2]  # MetricsCollector
    metrics = metrics_observer.get_metrics()
    for event, count in metrics.items():
        print(f"   {event}: {count} occurrences")
    print()

    # Displaying logs
    print("5. Generated logs:")
    logger_observer = subject.observers[0]  # LoggerObserver
    logs = logger_observer.get_logs()
    for log in logs:
        print(f"   {log['timestamp']} - {log['event']}: {log['data']}")
    print()

    # Removing an observer
    print("6. Removing an observer:")
    subject.remove_observer("email")
    print(f"   Number of active observers: {subject.get_observer_count()}")
    print()

    # Test with fewer observers
    print("7. Test with fewer observers:")
    subject.notify_observers("test_event", {"message": "Test without email notifier"})

    # Monitoring system simulation
    print("8. Monitoring system:")
    print("   Monitoring performance...")

    for i in range(5):
        subject.notify_observers(
            "performance_metric",
            {
                "cpu_usage": 20 + i * 5,
                "memory_usage": 60 + i * 2,
                "timestamp": datetime.now().isoformat(),
            },
        )

    # Displaying final metrics
    final_metrics = metrics_observer.get_metrics()
    print(f"\n   Final metrics: {final_metrics}")


if __name__ == "__main__":
    main()
