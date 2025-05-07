import asyncio
import os
import sys
import ccxt.async_support as ccxt
from database import Database

wait_time = 2  # seconds to wait between each check (MIN = 2)!!

exchanges = {
    "okx":ccxt.okx(),
    "bybit":ccxt.bybit({"options":{"defaultType":"spot"}}),
    "binance":ccxt.binance(),
    "kucoin":ccxt.kucoin(),
    "mexc":ccxt.mexc()
}

links = {
    "okx"    : "https://www.okx.com/ru/trade-spot/",
    "bybit"  : "https://www.bybit.com/ru-RU/trade/spot/",
    "binance": "https://www.binance.com/ru/trade/",
    "kucoin" : "https://www.kucoin.com/ru/trade/",
    "mexc"   : "https://www.mexc.com/ru-RU/exchange/"
}

link_dividers = {
    "okx"    : "-",#btc-usdt
    "bybit"  : "/",#BTC/USDT
    "binance": "_", #BTC_USDT
    "kucoin" : "-", #BTC-USDT
    "mexc"   : "_" #BTC_USDT
}

# symbols you want to trade
symbols = []
symbols_usdt = []
usdt_index = []
has_usdt = []
is_unfetchable = []
base_capital = 10000  # in USDT to calculate possible profit

# Helper function to calculate the profit
def calculate_profit(start_capital, exchange_fee, *orders):
    capital = start_capital
    for order in orders:
        if order['type'] == 'buy':
            capital = (capital - (capital * exchange_fee)) / order['price']
        else:
            capital = (capital - (capital * exchange_fee)) * order['price']
    return capital

async def get_last_prices(exchange):
    tasks = []
    tasks.append(exchange.fetch_tickers(symbols))
    results = await asyncio.gather(*tasks)
    return results

async def bot(exchange):
    # Fetch the last prices of symbols
    prices = await get_last_prices(exchange)
    temp = prices[0]
    data = []

    # Prepare symbol information for the order path
    symbol_info = {}
    for symbol in symbols:

        if temp[symbol]['last'] == None:
            symbol_info[symbol] = {
                'isActive': False,
                'price' : 0
            }
        else:
            symbol_info[symbol] = {
                'isActive': True,
                'price': float(temp[symbol]['last'])
            }
        
        # symbol_info[symbol] = {
        #     'price': float(temp[symbol]['last'])
        # }

    # Find profitable paths with exactly three steps
    for i in usdt_index:
        usdt_pair = symbols[i]
        pair0, base0 = usdt_pair.split('/')
        if symbol_info[usdt_pair]['isActive'] == False:
            continue
        

        for j in range(len(symbols)):
            if i == j:
                continue

            symbol1 = symbols[j]
            if symbol_info[symbol1]['isActive'] == False:
                continue
            pair1, base1 = symbol1.split('/')
            if base1 == "USDT" or (pair1 != pair0 and base1 != pair0):
                continue

            if pair1 not in has_usdt:
                continue

            for k in range(len(symbols)):
                if i == k or j == k:
                    continue

                symbol2 = symbols[k]
                if symbol_info[symbol2]['isActive'] == False:
                    continue
                pair2, base2 = symbol2.split('/')
                if base2 != 'USDT' or pair2 != base1:
                    continue

                exchange_fee = exchange.fees['trading']['taker']

                # Check if the trading path is profitable and contains exactly three steps
                profit = calculate_profit(
                    base_capital, exchange_fee,
                    {'price': symbol_info[usdt_pair]['price'], 'type': 'buy'},
                    {'price': symbol_info[symbol1]['price'], 'type': 'sell'},
                    {'price': symbol_info[symbol2]['price'], 'type': 'sell'}
                )

                if profit > base_capital:

                    profit = profit - base_capital
                    percentage = round((profit / base_capital)*100,3)
                    if percentage < 0.01:
                        continue
                    
                    data.append({
                                 "exchange": exchange.id,
                                 "step 1": {"symbol": usdt_pair, "price":symbol_info[usdt_pair]['price'], "Link": links[exchange.id]+usdt_pair.replace('/',link_dividers[exchange.id])},
                                 "step 2": {"symbol": symbol1, "price":symbol_info[symbol1]['price'], "Link": links[exchange.id]+symbol1.replace('/',link_dividers[exchange.id])},
                                 "step 3": {"symbol": symbol2, "price":symbol_info[symbol2]['price'], "Link": links[exchange.id]+symbol2.replace('/',link_dividers[exchange.id])},
                                 "profit": percentage})

                    # print("Profitable path found:")
                    # print(f"Step 1: Buy {usdt_pair} at price {symbol_info[usdt_pair]['price']}. Link: {links[exchange.id]+usdt_pair.replace('/',link_dividers[exchange.id])}")
                    # print(f"Step 2: Sell {symbol1} at price {symbol_info[symbol1]['price']}. Link: {links[exchange.id]+symbol1.replace('/',link_dividers[exchange.id])}")
                    # print(f"Step 3: Sell {symbol2} at price {symbol_info[symbol2]['price']}. Link: {links[exchange.id]+symbol2.replace('/',link_dividers[exchange.id])}")
                    # print(f"Total profit: {percentage}%")
                    # print()
    return data
async def check_requirements():
    print("Checking if exchanges support fetchTickers and the symbols we want to trade")
    for key, x in exchanges.items():
        if not x.has['fetchTickers']:
            print(x.id, "does not support fetchTickers")
            is_unfetchable.append(x.id)
        await x.load_markets()

def initialize(exchange):
    markets = exchange.markets_by_id
    index = 0

    for key, value in markets.items():
        for market in value:
            if market['active'] == True and market['type'] == 'spot':
                symbols.append(market['symbol'])
                if market['symbol'].endswith("USDT"):
                    symbols_usdt.append(market['symbol'])
                    temp = '' + market['symbol']
                    temp = temp.replace('/USDT', '')
                    has_usdt.append(temp)

    temp = symbols.copy()

    for symbol in temp:
        sym = '' + symbol
        x = sym.rsplit("/")
        # if x[0] == "BUSD" or x[1] == "BUSD" or x[0] == "TUSD" or x[1] == "TUSD":
        #     symbols.remove(symbol)
        if x[0] in has_usdt or x[1] in has_usdt:
            continue
        
        else:
            symbols.remove(symbol)

    for symbol in symbols:
        if symbol.endswith("USDT"):
            usdt_index.append(index)
        index += 1

async def main():
    await check_requirements()

    exchange_name = "binance" #change this to desired out of "exchanges"

    exchange = exchanges[exchange_name]
    initialize(exchange)

    print("Starting bot\n")
    while True:
        try:
            data = await bot(exchange)
            Database.insert_cardless_dict(data, False)
        except BaseException as e:
            print("Exception: ", e)
        await asyncio.sleep(wait_time)

asyncio.run(main())
