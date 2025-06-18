from datetime import datetime, timedelta
import queue
import threading
import time
import random

OrderRequestBody = tuple[str, datetime]
DeliveryTask = tuple[str, str]  # (order_name, provider)

# Available delivery providers
providers = ["uklon", "uber"]

# Track how many deliveries are being processed per provider
provider_load = {
    "uklon": 0,
    "uber": 0
}

# Use random provider selection or optimize based on load
USE_OPTIMIZED_PROVIDER_SELECTION = True

storage = {
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2,
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    # ...
}


class Scheduler:
    def __init__(self, delivery_queue: queue.Queue[DeliveryTask]):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery_queue = delivery_queue

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)
            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")
                provider = self.select_provider()
                self.delivery_queue.put((order[0], provider))
                provider_load[provider] += 1

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")

    def select_provider(self) -> str:
        if USE_OPTIMIZED_PROVIDER_SELECTION:
            return min(provider_load, key=provider_load.get)
        return random.choice(providers)


class DeliveryProcessor:
    def __init__(self, delivery_queue: queue.Queue[DeliveryTask]):
        self.delivery_queue = delivery_queue

    def process_deliveries(self) -> None:
        print("DELIVERY PROCESSOR STARTED...")

        while True:
            order_name, provider = self.delivery_queue.get(True)
            print(f"\n\t{order_name} PICKED UP BY {provider.upper()}")

            if provider == "uklon":
                time.sleep(5)
            elif provider == "uber":
                time.sleep(3)

            print(f"\n\t{order_name} DELIVERED BY {provider.upper()}")
            provider_load[provider] -= 1


def main():
    delivery_queue: queue.Queue[DeliveryTask] = queue.Queue()

    scheduler = Scheduler(delivery_queue)
    delivery_processor = DeliveryProcessor(delivery_queue)

    order_thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    delivery_thread = threading.Thread(target=delivery_processor.process_deliveries, daemon=True)

    order_thread.start()
    delivery_thread.start()

    while True:
        try:
            order_details = input("Enter order details (e.g., A 5): ")
            data = order_details.split(" ")
            order_name = data[0]
            delay = datetime.now() + timedelta(seconds=int(data[1]))
            scheduler.add_order(order=(order_name, delay))
        except (IndexError, ValueError):
            print("Invalid input. Use format like: A 5")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
