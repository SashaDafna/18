import requests
import json
from config import keys


class Exxe(Exception):
    pass


class Currencies:
    @staticmethod
    def get_price(amount: str, base: str, quote: str):
        if quote == base:
            raise Exxe(f'Нет перевода валюты в саму себя: {quote}={quote} 😐')
    
        try: 
            base_moneycode = keys[base.lower()]

        except KeyError:
            raise Exxe(f'Не могу обработать "{base}" как интересующую вас валюту, список доступных валют по запросу /values')
    
        try: 
            quote_moneycode = keys[quote.lower()]
    
        except KeyError:
            raise Exxe(f'Не могу обработать "{quote}" как валюту расчёта, список доступных валют по запросу /values')
    
        try:
            amount = float(amount)
            
        except ValueError:
            raise Exxe(f'Не могу обработать "{amount}" числом:\nнапишите сколько надо валюты по типу  1  или  2.345')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_moneycode}&tsyms={quote_moneycode}')
        total_quote = json.loads(r.content)[keys[quote.lower()]] * amount

        return total_quote
