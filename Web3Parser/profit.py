def profit_calculation(buyArray, sellArray, capital):
    profits = []
    if len(buyArray) == 0 or len(sellArray) == 0:
        return []

    for sellOffer in sellArray:
        for buyOffer in buyArray:

            if buyOffer['Exchange'] == sellOffer['Exchange']:
                type = buyOffer['Exchange']
            else:
                type = 'International'

            buyBanks = buyOffer['Banks']
            sellBanks = sellOffer['Banks']

            fiat = sellOffer['Fiat']  
            asset = sellOffer['Asset']

            sellPrice = float(sellOffer['Price'])
            sellAmount = float(sellOffer['Amount'])
            sellBotLim = float(sellOffer['Bottom Limit'])
            sellTopLim = float(sellOffer['Top Limit'])

            buyPrice = float(buyOffer['Price'])
            buyAmount = float(buyOffer['Amount'])
            buyBotLim = float(buyOffer['Bottom Limit'])
            buyTopLim = float(buyOffer['Top Limit'])

            if sellPrice > buyPrice:
                if sellBotLim <= capital and buyBotLim <= capital:
                        if sellTopLim >= buyBotLim and buyTopLim >= sellBotLim:
                            newCapital = min(sellTopLim, buyTopLim, capital)
                            assets = newCapital / buyPrice
                            profit = assets * sellPrice
                            profitPercentage = round(((profit - newCapital) / newCapital)*100, 2)
                            profits.append({
                                'Buy Link: ': buyOffer['Link'],
                                'Sell link: ': sellOffer['Link'],
                                'Buy Price': buyPrice,
                                'Sell Price': sellPrice,
                                'Money Spent': assets * buyPrice,
                                'Money Received': profit,
                                'Profit Percentage': str(profitPercentage) + '%',
                                'Amount to BUY/SELL': assets,
                                'Fiat': fiat,
                                'Asset': asset,
                                'Buy banks': buyBanks,
                                'Sell banks': sellBanks,
                                'Type': type
                            })

    profits = sorted(profits, key=lambda x: x['Profit Percentage'])
    return profits
