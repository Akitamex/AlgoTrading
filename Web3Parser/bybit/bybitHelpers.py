import requests
import json

def banksMap():
    banks_map = {}
    result = json.loads(requests.post('https://api2.bybit.com/spot/api/v1/otc/payment/broker_config_list').text)['result']
    for item in result:
        banks_map[str(item['paymentType'])] = item['paymentName']

    return banks_map

def assets():
    result = json.loads(requests.get('https://api2.bybit.com/spot/api/otc/config').text)['result']['token']
    assets = []
    for res in result:
        if res['maxQuote'] != "0":
            assets.append(res['tokenName'])
    return assets