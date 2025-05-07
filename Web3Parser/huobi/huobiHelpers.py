import json
import requests

def filter(fiat = 'KZT'):


    data = {
        'type': 'currency,marketQuery,pay,allCountry,coin'
    }

    result = requests.get("https://www.huobi.com/-/x/otc/v1/data/config-list", params=data)
    result = result.json()

    return result

def assets(fiat):
    assets = {}

    with open('HuobiAssets.js') as file:
        js_content = file.read()

    parsed_data = json.loads(js_content)
    for data in parsed_data:
        for currency in data['quoteAsset']:
            if currency['name'] in assets:
                assets[currency['name']].append(data['cryptoAsset']['name'])
            else:
                assets[currency['name']] = [data['cryptoAsset']['name']]

    return assets[fiat]
