import json
import requests

def buySell(allBanks, fiat = 'KZT', asset = 'USDT'):
    rows = 20

    types = ['BUY', 'SELL']
    
    exchange = 'Binance'

    buyDataArray = []
    sellDataArray = []

    page = 1
    while page <= 1:
        for type in types:
            data = {
                "fiat": fiat,
                "page": page,
                "rows": rows,
                "tradeType": type,
                "asset": asset,
                "countries": [],
                "proMerchantAds": False,
                "publisherType": None,
                "payTypes": []
            }
            
            outDataArray = []
            if type == 'BUY':
                outDataArray = buyDataArray
            else:
                outDataArray = sellDataArray
            
            result = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json=data)
            result = result.json()
            
            result = result['data']
            for res in result:                

                outData = {
                    'Exchange': None,
                    'Fiat': None,
                    'Asset': None,
                    'Banks': None,
                    'Type': None,
                    'Price': None,
                    'Amount': None,
                    'Bottom Limit': None,
                    'Top Limit': None,
                    'Nickname': None,
                    'Monthly Orders': None,
                    'Completion Rate': None,
                    'Link': None,
                }

                advertisement = res['adv']
                advertiser = res['advertiser']

                
                outData['Monthly Orders'] = advertiser['monthOrderCount']
                if outData['Monthly Orders'] < 20:
                    continue
                outData['Completion Rate'] = (float(advertiser['monthFinishRate'])*100)     
                if outData['Completion Rate'] < 90:
                    continue
                outData['Link'] = "https://p2p.binance.com/ru/advertiserDetail?advertiserNo=" + advertiser['userNo']

 

                banks = []
                for tradeMethod in advertisement['tradeMethods']:
                    if tradeMethod['tradeMethodName'] != None:
                        banks.append(tradeMethod['tradeMethodName'])
                outData['Banks'] = banks
                
                valid = False
                for i in allBanks:
                    for j in banks:
                        if i.lower() == j.lower():
                            valid = True
                            break
                    if valid:
                        break
                if valid != True:
                    continue

                outData['Exchange'] = exchange
                outData['Fiat'] = fiat
                outData['Asset'] = asset  

                outData['Type'] = type
                outData['Price'] = advertisement['price']
                outData['Amount'] = advertisement['tradableQuantity']
                outData['Bottom Limit'] = advertisement['minSingleTransAmount']
                outData['Top Limit'] = advertisement['dynamicMaxSingleTransAmount']
                outData['Nickname'] = advertiser['nickName']
                
                outDataArray.append(outData)
                       
        page += 1
                
    buyDataArray = sorted(buyDataArray, key=lambda x: x['Price'])[0:30]
    sellDataArray = sorted(sellDataArray, key=lambda x: x['Price'], reverse=True)[0:30]
    data = [buyDataArray, sellDataArray]
    return data