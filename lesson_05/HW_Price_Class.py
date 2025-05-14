class Price:
    # Fictitious exchange rates against CHF
    exchange_rates = {
        "CHF": 1.0,
        "USD": 1.1,
        "EUR": 1.05,
        "GBP": 1.25,
    }

    def __init__(self, value: float, currency: str):
        assert value >= 0, f"The price's value `{value}` cannot be less than zero."
        assert Price.exchange_rates.get(currency), f"The currency `{currency}` is not supported."

        self.value = value
        self.currency = currency

    def to_chf(self):
        return self.value * Price.exchange_rates.get(self.currency)

    def from_chf(self):
        return self.value / Price.exchange_rates.get(self.currency)

    def __add__(self, other):
        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            chf_value = self.to_chf() + other.to_chf()
            add_value = chf_value / Price.exchange_rates.get(self.currency)
            return Price(round(add_value, 2), self.currency)

    def __sub__(self, other):
        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            chf_value = self.to_chf() - other.to_chf()
            sub_value = chf_value / Price.exchange_rates.get(self.currency)
            return Price(round(sub_value, 2), self.currency)

    def __repr__(self):
        return f"{self.value} {self.currency}"


if __name__ == '__main__':
    try:
        p1 = Price(100, "EUR")
        p2 = Price(150, "USD")
    except AssertionError as msg:
        print(msg)
    else:
        p3 = p1 + p2
        p4 = p2 - p1

        print(p1, p2, p3, p4, sep="\n")
