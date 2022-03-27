import requests


class APIException(Exception):
    pass


class Conv:
    @staticmethod
    def conversion(base, quote):
        url = "https://currency-exchange.p.rapidapi.com/exchange"
        headers = {
            'x-rapidapi-host': "currency-exchange.p.rapidapi.com",
            'x-rapidapi-key': "031c2a0b2amsh5300b8457a59036p170ee6jsn27de70768800"
        }
        querystring = {"format": "json", "from": base, "to": quote, "amount": "1"}

        return requests.request("GET", url, headers=headers, params=querystring).text

    @staticmethod
    def get_price(base, quote, amount):
        return f'{amount} {base} is {round(float(amount) * float(Conv.conversion(base, quote)), 2)} {quote}! Good luck and buy ' \
               f'something cute! '

    @staticmethod
    def currency_list():
        url = "https://currency-exchange.p.rapidapi.com/listquotes"

        headers = {
            'x-rapidapi-host': "currency-exchange.p.rapidapi.com",
            'x-rapidapi-key': "031c2a0b2amsh5300b8457a59036p170ee6jsn27de70768800"
        }

        response = requests.request("GET", url, headers=headers)
        a = response.text  # manual reformatting
        a = a.replace('''"''', '')
        a = a.replace(''',''', ' ')
        a = a.replace('''[''', '')
        a = a.replace(''']''', '')
        return a
