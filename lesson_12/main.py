import queue
import threading
import time
import random
from datetime import datetime, timedelta

OrderRequestBody = tuple[str, datetime]
ProviderRequestBody = tuple[str, OrderRequestBody]

available_providers = ("uklon", "uber")

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
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery: queue.Queue[ProviderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                # print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")
                provider = random.choice(available_providers)
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT BY {provider.upper()}")
                self.add_delivery(provider=(provider, order))

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")

    def process_delivery(self) -> None:
        provider = self.delivery.get(True)
        if provider[0] == "uklon":
            time.sleep(5)
        elif provider[0] == "uber":
            time.sleep(3)
        print(f"\n\t{provider[1][0]} DELIVERED BY {provider[0].upper()}")

    def add_delivery(self, provider: ProviderRequestBody) -> None:
        # print(f"\n\t{provider[1][0]} DELIVERED BY {provider[0].upper()}")
        self.delivery.put(provider)


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread2 = threading.Thread(target=scheduler.process_delivery, daemon=True)
    thread.start()
    thread2.start()

    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
