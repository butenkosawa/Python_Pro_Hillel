class Price:
    # Fictitious exchange rates against CHF
    exchange_rates = {
        "CHF": 1.0,
        "USD": 1.1,
        "EUR": 1.05,
        "GBP": 1.25,
    }

    def __init__(self, value: float, currency: str):
        if value < 0:
            raise ValueError(f"The price's value `{value}` cannot be less than zero.")
        if not Price.exchange_rates.get(currency):
            raise ValueError(f"The currency `{currency}` is not supported.")

        self.value = value
        self.currency = currency


    def convert_to_chf(self):
        return self.value * Price.exchange_rates.get(self.currency)

    def convert_from_chf(self):
        return self.value / Price.exchange_rates.get(self.currency)

    def __add__(self, other):
        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            chf_value = self.convert_to_chf() + other.convert_to_chf()
            add_value = chf_value / Price.exchange_rates.get(self.currency)
            return Price(round(add_value, 2), self.currency)

    def __sub__(self, other):
        if self.currency == other.currency:
            sub_value = self.value - other.value
            if sub_value >= 0:
                return Price(sub_value, self.currency)
            else:
                print("Сannot subtract a larger price from a smaller price")
        else:
            chf_value = self.convert_to_chf() - other.convert_to_chf()
            if chf_value >= 0:
                sub_value = chf_value / Price.exchange_rates.get(self.currency)
                return Price(round(sub_value, 2), self.currency)
            else:
                print("Сannot subtract a larger price from a smaller price")

    def __eq__(self, other):
        return True if self.convert_to_chf() == other.convert_to_chf() else False

    def __repr__(self):
        return f"{self.value} {self.currency}"


if __name__ == '__main__':
    try:
        p1 = Price(100, "EUR")
        p2 = Price(150, "USD")
        p5 = Price(100, "EUR")
    except ValueError as msg:
        print(msg)
    else:
        p3 = p1 + p2
        p4 = p2 - p1

        print(p1, p2, p3, p4, sep="\n")

        print(p5 == p1)
        print(p5 == p2)
