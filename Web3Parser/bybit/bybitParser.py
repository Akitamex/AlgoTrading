import requests
import json

def buySell(banksMap, allBanks, fiat = 'KZT', asset = 'USDT'):
    rows = 30
    type = ['SELL', 'BUY']    
    banksDictionary = banksMap
    # allBanks = fiatBanks(fiat)[0: 10]
    exchange = 'ByBit'
    
    buyDataArray = []
    sellDataArray = []

    for t in range(2):
        data = {
            "userId": "",
            "tokenId": asset,   #Asset
            "currencyId": fiat,  #Fiat
            "payment": [],   #Banks
            "side": str(t), #type: 1 = BUY; 0 = SELL
            "size": str(rows),  
            "page": "1",
            "amount": "",
            "authMaker": False,
            "canTrade": False
        }
        
        outDataArray = []
        if type[t] == 'BUY':
            outDataArray = buyDataArray
        else:
            outDataArray = sellDataArray
        
        result = json.loads(requests.post('https://api2.bybit.com/fiat/otc/item/online', json=data).text)['result']['items']
        for item in result:
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

            outData['Monthly Orders'] = item['recentOrderNum']
            if outData['Monthly Orders'] < 20:
                continue
            outData['Completion Rate'] = (float(item['recentExecuteRate']))     
            if outData['Completion Rate'] < 90:
                continue

            
            banks = []
            for tradeMethod in item['payments']:
                banks.append(banksDictionary[str(tradeMethod)])
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
            outData['Type'] = type[t]
            outData['Price'] = item['price']
            outData['Amount'] = item['lastQuantity']
            outData['Bottom Limit'] = item['minAmount']
            outData['Top Limit'] = item['maxAmount']
            outData['Nickname'] = item['nickName']
            outData['Link'] = "https://www.bybit.com/fiat/trade/otc/profile/" + item['userId'] + "/" + asset + "/" + fiat + "/item"
            
            outDataArray.append(outData)
       
    buyDataArray = sorted(buyDataArray, key=lambda x: x['Price'])
    sellDataArray = sorted(sellDataArray, key=lambda x: x['Price'], reverse=True)
    data = [buyDataArray, sellDataArray]
    return data