import requests

def buySell(all_info, allBanks, fiat = 'KZT', asset = 'USDT'):
    buyDataArray = []
    sellDataArray = []
    
    for x in all_info['data']['currency']:
        if x['nameShort'] == fiat:
            IDs = x
            break          
    
    fiat_id = IDs['currencyId']

    for x in all_info['data']['coin']:
        if x['coinCode'] == asset:
            asset_id = x['coinId']
            break
        
    page = 1
    while page <= 3:
        result = parserHelper(allBanks, fiat, asset, fiat_id, asset_id, 'BUY', page)

        if result == 'stop':
            break

        for res in result:
            buyDataArray.append(res)

        page += 1

    page = 1
    while page <= 3:
        result = parserHelper(allBanks, fiat, asset, fiat_id, asset_id, 'SELL', page)

        if result == 'stop':
            break

        for res in result:
            sellDataArray.append(res)

        page += 1

    buyDataArray = sorted(buyDataArray, key=lambda x: x['Price'])
    sellDataArray = sorted(sellDataArray, key=lambda x: x['Price'], reverse=True)
    data = [buyDataArray, sellDataArray]
    return data


def parserHelper(allBanks, fiat, asset, fiat_id, asset_id, type, page):
    array = []
    if type == 'BUY':
        t = 'SELL'
    else:
        t = 'BUY'
    data = {
        'coinId': asset_id,
        'currency': fiat_id,
        'tradeType': t,
        'currPage': page,
        'payMethod': 0,
        'acceptOrder': 0,
        #'country': ,
        'blockType': 'general',
        'online': 1,
        'range': 0,
        #'amount': ,
        'onlyTradable': 'false',
        'isFollowed': 'false'                
    }
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    result = requests.get("https://www.huobi.com/-/x/otc/v1/data/trade-market", params=data, headers=header).json()['data']
    if len(result) == 0:
        return 'stop'
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

        outData['Monthly Orders'] = item['tradeMonthTimes']
        outData['Completion Rate'] = (float(item['orderCompleteRate']))     
        
        banks = []
        for tradeMethod in item['payMethods']:
            banks.append(tradeMethod['name'])
        outData['Banks'] = banks
        outData['Exchange'] = 'Huobi'
        outData['Fiat'] = fiat
        outData['Asset'] = asset   
        outData['Type'] = type
        outData['Price'] = item['price']
        outData['Amount'] = item['tradeCount']
        outData['Bottom Limit'] = item['minTradeLimit']
        outData['Top Limit'] = item['maxTradeLimit']
        outData['Nickname'] = item['userName']
        outData['Link'] = "https://www.huobi.com/en-us/fiat-crypto/trader/" + str(item['uid'])


        if outData['Monthly Orders'] < 20:
            continue
        
        if outData['Completion Rate'] < 90:
            continue

        

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
        
        array.append(outData)

    return array