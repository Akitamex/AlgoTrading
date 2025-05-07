import json
import requests

def fiatFilter(fiat = 'KZT'):
    data = {
        "fiat": fiat
    }

    result = requests.post("https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/filter-conditions", json=data)

    result = json.loads(result.text)['data']

    return result


def fiatBanks(fiat = 'KZT'):
    data = fiatFilter(fiat)['tradeMethods']

    list = []

    for x in data:
        list.append(x['tradeMethodName'])

    return list[0: 10]

def assets(fiat = 'KZT'):
    data = {
        "fiat": fiat
    }

    result = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/portal/config", json=data)

    result = json.loads(result.text)

    data = result['data']['areas'][0]['tradeSides'][1]['assets']

    list = []

    for x in data:
        list.append(x['asset'])

    return list