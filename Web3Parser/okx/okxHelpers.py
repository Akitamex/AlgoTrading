import requests

def fiat_filter(fiat = 'KZT'):
    data = {
        'quoteCurrency': fiat
    }

    result = requests.get("https://www.okx.com/v3/c2c/configs/receipt/templates", params=data)
    result = result.json()['data']
    return result

def fiatBanks(fiat = 'KZT'):
    data = fiat_filter(fiat)

    banks = {}

    for x in data:
        banks[x['paymentMethod']] = x['paymentMethodDescription']

    return banks

def assets(fiat = 'KZT'):
    data = {
        'type': '2',
        'quote': fiat,
    }
    result = requests.get("https://www.okx.com/v3/c2c/currency/pairs", params=data)
    result = result.json()['data']
    assets = []
    for res in result:
        assets.append(res['baseCurrency'])
    return assets