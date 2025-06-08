import requests

apikey = '51ANUD4JT33OPGN7'
currency_exchange_rate = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={0}&to_currency={1}&apikey={2}'
currencies = 'https://www.alphavantage.co/physical_currency_list'
response = requests.get(currencies)
currencies = response.content.decode('utf-8')


class Price:
    def __init__(self, value: float, currency: str):
        if value < 0:
            raise ValueError(f"The price's value `{value}` cannot be less than zero.")
        if currency not in currencies:
            raise ValueError(f"The currency `{currency}` is not supported.")

        self.value = value
        self.currency = currency

    def convert_to_chf(self) -> tuple[float, float]:
        response = requests.get(currency_exchange_rate.format(self.currency, 'CHF', apikey))
        rate_data = response.json().get('Realtime Currency Exchange Rate')
        exchange_rate = float(rate_data.get('5. Exchange Rate'))
        return self.value * exchange_rate, exchange_rate

    def convert_from_chf(self) -> tuple[float, float]:
        response = requests.get(currency_exchange_rate.format('CHF', self.currency, apikey))
        rate_data = response.json().get('Realtime Currency Exchange Rate')
        exchange_rate = float(rate_data.get('5. Exchange Rate'))
        return self.value * exchange_rate, exchange_rate

    def __add__(self, other: 'Price') -> 'Price':
        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            chf_value = self.convert_to_chf()[0] + other.convert_to_chf()[0]
            add_value = chf_value / self.convert_to_chf()[1]
            return Price(round(add_value, 2), self.currency)

    def __sub__(self, other: 'Price') -> 'Price | None':
        if self.currency == other.currency:
            sub_value = self.value - other.value
            if sub_value >= 0:
                return Price(sub_value, self.currency)
            else:
                print('You cannot subtract a higher price from a lower price')
                return None
        else:
            chf_value = self.convert_to_chf()[0] - other.convert_to_chf()[0]
            if chf_value >= 0:
                sub_value = chf_value / self.convert_to_chf()[1]
                return Price(round(sub_value, 2), self.currency)
            else:
                print("You cannot subtract a higher price from a lower price")
                return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Price):
            return NotImplemented
        return self.convert_to_chf()[0] == other.convert_to_chf()[0]

    def __repr__(self):
        return f"{self.value} {self.currency}"


if __name__ == '__main__':
    try:
        p1 = Price(100, "EUR")
        p2 = Price(150, "USD")
    except ValueError as msg:
        print(msg)
    else:
        p3 = p1 + p2
        p4 = p2 - p1

        print(p1, p2, p3, p4, sep="\n")
