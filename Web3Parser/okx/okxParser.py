import requests

def buySell(banksMap, allBanks, fiat = 'KZT', asset  = 'USDT'):
    rows = 30
    types = ['SELL', 'BUY'] 
    exchange = 'OKX'
    
    buyDataArray = []
    sellDataArray = []
    for type in types:
        rev_type = ""
        sort_type = ""
        if type == "BUY":
            sort_type = "price_desc"
            rev_type = "sell"
        else:
            sort_type = "price_asc"
            rev_type = "buy"
        data = {
            "side": rev_type,
            "paymentMethod": "all",
            "userType": all,
            "hideOverseasVerificationAds": "false",
            "sortType": sort_type,
            "urlId": 0,
            "limit": 1000,
            "cryptoCurrency": asset,
            "fiatCurrency": fiat,
            "currentPage": 1,
            "numberPerPage": rows
        }

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        outDataArray = []
        if type == 'BUY':
            outDataArray = buyDataArray
        else:
            outDataArray = sellDataArray

        result = requests.get("https://www.okx.com/v3/c2c/tradingOrders/getMarketplaceAdsPrelogin", params=data,headers=header).json()['data'][rev_type]
   

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

            outData['Monthly Orders'] = item['completedOrderQuantity']
            if outData['Monthly Orders'] < 20:
                continue
            outData['Completion Rate'] = (float(item['completedRate'])*100)     
            if outData['Completion Rate'] < 90:
                continue

            
            banks = []
            for tradeMethod in item['paymentMethods']:
                banks.append(banksMap[tradeMethod])
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
            outData['Price'] = item['price']
            outData['Amount'] = item['availableAmount']
            outData['Bottom Limit'] = item['quoteMinAmountPerOrder']
            outData['Top Limit'] = item['quoteMaxAmountPerOrder']
            outData['Nickname'] = item['nickName']
            outData['Link'] = "https://www.okx.com/ru/p2p/ads-merchant?publicUserId=" + item['publicUserId']
            
            outDataArray.append(outData)
       

    buyDataArray = sorted(buyDataArray, key=lambda x: x['Price'])
    sellDataArray = sorted(sellDataArray, key=lambda x: x['Price'], reverse=True)
    data = [buyDataArray, sellDataArray]
    return data