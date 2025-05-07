import asyncio
import os
from random import randint
import sys
from pprint import pprint
import time
from database import Database

# Как там с деньгами
# Выбор всех бирж которые мы подключаем
# Валюты (деньги), параметр на какой бирже он есть
# Деньги

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt

wait_time = 2 # seconds to wait between each check (MIN = 2)!!

# exchanges you want to use to look for arbitrage opportunities
exchanges = [
    ccxt.okx(),
    ccxt.bybit({"options":{"defaultType":"spot"}}),
    ccxt.binance(),
    ccxt.kucoin(),
    ccxt.bitmart(),
    ccxt.gate(),
    ccxt.mexc()
]

# symbols you want to trade
symbols = [
    "BTC/USDT",
    "LTC/USDT",
    "DOGE/USDT",
    "SHIB/USDT",
    "SOL/USDT",
    "ETH/USDT",
    "ADA/USDT",
    "DOT/USDT",
    "UNI/USDT",
    "LINK/USDT",
    "SUTER/USDT",
    "GMEE/USDT",
    "FEAR/USDT",
]

# order sizes for each symbol, adjust it to your liking
order_sizes = {
    "BTC/USDT": 0.0001,
    "LTC/USDT": 0.001,
    "DOGE/USDT": 10,
    "SHIB/USDT": 100000,
    "SOL/USDT": 0.01,
    "ETH/USDT": 0.001,
    "ADA/USDT": 0.1,
    "DOT/USDT": 0.01,
    "UNI/USDT": 0.01,
    "LINK/USDT": 0.01,
    "SUTER/USDT": 0.001,
    "GMEE/USDT":0.001,
    "FEAR/USDT":0.001,

}

links = {                                           #formats:
    "okx"    : "https://www.okx.com/ru/trade-spot/",#btc-usdt
    "bybit"  : "https://www.bybit.com/ru-RU/trade/spot/",#BTC/USDT
    "binance": "https://www.binance.com/ru/trade/", #BTC_USDT
    "kucoin" : "https://www.kucoin.com/ru/trade/", #BTC-USDT   
    "bitmart": "https://www.bitmart.com/trade/ru-RU?layout=pro&theme=dark&symbol=", #BTC_USDT
    "gate"   : "https://www.gate.io/ru/trade/", #BTC_USDT
    "mexc"   : "https://www.mexc.com/ru-RU/exchange/" #BTC_USDT
}

link_dividers = {
    "okx"    : "-",#btc-usdt
    "bybit"  : "/",#BTC/USDT
    "binance": "_", #BTC_USDT
    "kucoin" : "-", #BTC-USDT   
    "bitmart": "_", #BTC_USDT
    "gate"   : "_", #BTC_USDT
    "mexc"   : "_" #BTC_USDT
}

unsupported = {}

# supported = {
#     "BTC/USDT": [],
#     "LTC/USDT": [],
#     "DOGE/USDT": [],
#     "SHIB/USDT": [],
#     "SOL/USDT": [],
#     "ETH/USDT": [],
#     "ADA/USDT": [],
#     "DOT/USDT": [],
#     "UNI/USDT": [],
#     "LINK/USDT": [],
#     "SUTER/USDT": [],
#     "GMEE/USDT": [],
# }

async def get_last_prices():
    tasks = []
    for exchange in exchanges:
        temp = symbols.copy()
        temp_copy = temp.copy()

        for x in temp_copy:
            if exchange.id in unsupported:    
                if x in unsupported[exchange.id]:
                    temp.remove(x)
        tasks.append(exchange.fetch_tickers(temp))

    results = await asyncio.gather(*tasks)
    return results

async def bot():
    # print(unsupported,'\n')
    prices = await get_last_prices()
    data = []
    for symbol in symbols:
        ms = int(time.time() * 1000)


        symbol_prices = []
        symbol_index = []
        index = 0
        for exchange_prices in prices:
            
            if symbol in exchange_prices:
                symbol_prices.append(exchange_prices[symbol]['last'])
                symbol_index.append(index)
            index += 1

        min_price = min(symbol_prices)
        max_price = max(symbol_prices)

        order_size = order_sizes[symbol]

        min_exchange = exchanges[symbol_index[symbol_prices.index(min_price)]]
        max_exchange = exchanges[symbol_index[symbol_prices.index(max_price)]]

        # calculate min exchange taker fee
        # warning: you need to manually check if there are special campaign fees 
        min_exchange_fee = min_exchange.fees['trading']['taker']
        min_fee = order_size * min_price * min_exchange_fee

        max_exchange_fee = max_exchange.fees['trading']['taker']
        max_fee = order_size * max_price * max_exchange_fee

        price_profit = max_price - min_price
        profit = (price_profit * order_size) - (min_fee) - (max_fee)

        if (profit > 0): # not taking into account slippage or order book depth
            tempBuy = '' + symbol
            tempSell = '' + symbol

            tempBuy = tempBuy.replace('/' , link_dividers.get(min_exchange.id))
            tempSell = tempSell.replace('/' , link_dividers.get(max_exchange.id))

            data.append({"symbol": symbol, "profit": profit, "buy_from":min_exchange.id, "buy_price":min_price, "sell_from":max_exchange.id,
                          "sell_price": max_price, "buy_link" : links.get(min_exchange.id) + tempBuy, "sell_link": links.get(max_exchange.id) + tempSell})
            
            #data.append({"symbol": symbol, "profit": profit, "buy_from":min_exchange.id, "buy_price":min_price, "sell_from":max_exchange.id, "sell_price": max_price})
            #print( symbol, "profit:", profit, "Buy", min_exchange.id, min_price, "Sell", max_exchange.id, max_price)
            
        #else:
            #data.append({"symbol": symbol, "has_profit": 0})
            #print(str(ms), symbol, "no arbitrage opportunity")
    return data
async def check_requirements():
    print("Checking if exchanges support fetchTickers and the symbols we want to trade")
    for exchange in exchanges:
        if not exchange.has['fetchTickers']:
            print(exchange.id, "does not support fetchTickers")
            sys.exit()
        await exchange.load_markets()
        
        for symbol in symbols:
            if symbol not in exchange.markets:
                #print(exchange.id, "does not support", symbol,"\n")
                if exchange.id not in unsupported:
                    temp = [symbol]
                    unsupported.update({exchange.id : temp})
                else:
                    unsupported[exchange.id].append(symbol)
            
                #sys.exit()

async def main():    
    Database.exchange_to_db(list(links.keys()))
    
    result = Database.symbols_from_db()
        
    symbols = result['symbols']
    order_sizes = result['order_sizes']
    
    await check_requirements()
    while True:
        try:
            data = await bot()
            Database.insert_cardless_dict(data, True)
        except BaseException as e:
            print("Exception: ", e)
        await asyncio.sleep(wait_time)

asyncio.run(main())
