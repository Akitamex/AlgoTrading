import threading
import concurrent.futures
import time
import asyncio
import psycopg2
from binance import binanceHelpers as binH
from binance import binanceParser as binP
from bybit import bybitHelpers as bbH
from bybit import bybitParser as bbP
from huobi import huobiHelpers as hH
from huobi import huobiParser as hP
from okx import okxHelpers as okxH
from okx import okxParser as okxP
from profit import profit_calculation
from printDictionaryOrList import *
from database import Database


lock = threading.Lock()

# banks                     Банки по которым фильтруются офферы. Топ 10 самых ликвидных, берутся с Бинанса

# binanceAssets             Все доступные ассеты для определенного фиата для Бинанса

# binanceBuy                Дикшонари бай офферов из Бинанса, ключ: Фиат+Ассет. Сортировка по возрастанию

# binanceSell               Дикшонари селл офферов из Бинанса, ключ: Фиат+Ассет. Сортировка по убыванию

# allCouplesBuy             Дикшонари всех бай офферов, ключ: Фиат+Ассет. Сортировка по возрастанию

# allCouplesSell            Дикшонари всех селл офферов, ключ: Фиат+Ассет. Сортировка по убыванию

# bybitBanksMap             Мапа банков для Байбита, офферы хранят Айди банков вместо названий, нужна
#                           для перевода. Фиат не нужен. Можно фетчить раз в сутки

# bybitAssets               Все доступные ассеты для Байбита. Для всех фиатов. Можно фетчить раз в сутки

# bybitBuy                  Дикшонари бай офферов из Байбита, ключ: Фиат+Ассет. Сортировка по возрастанию

# bybitSell                 Дикшонари селл офферов из Байбита, ключ: Фиат+Ассет. Сортировка по убыванию

# all_info                  Вспомогательные данные для Хуеби, нужны для перевода Фиата и Ассета
#                           в их Айди для АПИшки. Фетчить можно раз в сутки

# huobiAssets               Все доступные ассеты для определенного фиата для Хуеби. Можно фетчить раз в сутки

# huobiBuy                  Дикшонари бай офферов из бинанса, ключ: Фиат+Ассет. Сортировка по возрастанию

# huobiSell                 Дикшонари селл офферов из бинанса, ключ: Фиат+Ассет. Сортировка по убыванию

# okxBanksMap               Мапа банков ОКХ, переводит укороченные названия банков, 
#                                  необходима для совпадения с банками Бинанса

# okxAssets                 Все доступные ассеты для определенного фиата для ОКХ

# okxBuy                    Дикшонари бай офферов из бинанса, ключ: Фиат+Ассет. Сортировка по возрастанию

# okxSell                   Дикшонари селл офферов из бинанса, ключ: Фиат+Ассет. Сортировка по убыванию

# fiat                      Фиат глобальный чтобы был доступен для доступа во вспомогательных функциях
#                                  меняется на нужный в Мейн функции

def binance(fiat, banks, binanceAssets, binanceBuy, binanceSell):

    num_threads = len(binanceAssets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(binP.buySell, banks, fiat, asset) for asset in binanceAssets]

        results = [future.result() for future in futures]

    counter = 0

    for asset in binanceAssets:
        data = results[counter]

        binanceBuy[fiat + '+' + asset] = data[0]
        binanceSell[fiat + '+' + asset] = data[1]
        
        counter += 1

def bybit(bybitBanksMap, banks, fiat, bybitAssets, bybitBuy, bybitSell):

    num_threads = len(bybitAssets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(bbP.buySell, bybitBanksMap, banks, fiat, asset) for asset in bybitAssets]

        results = [future.result() for future in futures]

    counter = 0

    for asset in bybitAssets:
        data = results[counter]

        bybitBuy[fiat + '+' + asset] = data[0]
        bybitSell[fiat + '+' + asset] = data[1]

        counter += 1

def huobi(all_info, banks, fiat, huobiAssets, huobiBuy, huobiSell):
    
    num_threads = len(huobiAssets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(hP.buySell, all_info, banks, fiat, asset) for asset in huobiAssets]

        results = [future.result() for future in futures]

    counter = 0

    for asset in huobiAssets:
        data = results[counter]

        huobiBuy[fiat + '+' + asset] = data[0]
        huobiSell[fiat + '+' + asset] = data[1]

        counter += 1

def okx(okxBanksMap, banks, fiat, okxAssets, okxBuy, okxSell):
    
    num_threads = len(okxAssets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(okxP.buySell, okxBanksMap, banks, fiat, asset) for asset in okxAssets]

        results = [future.result() for future in futures]

    counter = 0

    for asset in okxAssets:
        data = results[counter]

        okxBuy[fiat + '+' + asset] = data[0]
        okxSell[fiat + '+' + asset] = data[1]

        counter += 1

def merger(allCouplesBuy, allCouplesSell, dictionary, type):
    with lock:
        if type == 'SELL':            
            for (k, v) in dictionary.items():
                if k in allCouplesSell:
                    allCouplesSell[k] = sorted((allCouplesSell[k] + v), key=lambda x: x['Price'], reverse=True)
                else:
                    allCouplesSell[k] = v

        elif type == 'BUY':
            for (k, v) in dictionary.items():
                if k in allCouplesBuy:
                    allCouplesBuy[k] = sorted((allCouplesBuy[k] + v), key=lambda x: x['Price'])
                else:
                    allCouplesBuy[k] = v


def parseFiat(fiat = 'KZT'):
    banks = binH.fiatBanks(fiat)
    binanceAssets = binH.assets(fiat)
    okxAssets = okxH.assets(fiat)
    allCouplesBuy = {}
    allCouplesSell = {}
    binanceBuy = {}
    binanceSell = {}
    okxBuy = {}
    okxSell = {}
    okxBanksMap = okxH.fiatBanks(fiat)

#

    # bybitBuy = {}
    # bybitSell = {}
    huobiBuy = {}
    huobiSell = {}
    # bybitAssets = bbH.assets()
    huobiAssets = hH.assets(fiat)
    # bybitBanksMap = bbH.banksMap()
    all_info = hH.filter(fiat)

#
    allAssets = list(set(binanceAssets + okxAssets + huobiAssets))
    
    profits = []

    function_arguments = {
        binance: (fiat, banks, binanceAssets, binanceBuy, binanceSell),
        okx: (okxBanksMap, banks, fiat, okxAssets, okxBuy, okxSell),
        # bybit: (bybitBanksMap, banks, fiat, bybitAssets, bybitBuy, bybitSell),
        huobi: (all_info, banks, fiat, huobiAssets, huobiBuy, huobiSell),
    }
    threads = []
    for func, args in function_arguments.items():
        thread = threading.Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    buys = [binanceBuy, okxBuy, huobiBuy] #, bybitBuy, huobiBuy]
    sells = [binanceSell, okxSell, huobiSell] #, bybitSell, huobiSell]

    num_threads = len(buys)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(merger, allCouplesBuy, allCouplesSell, dictionary, 'BUY') for dictionary in buys]

        concurrent.futures.wait(futures)

    num_threads = len(sells)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(merger, allCouplesBuy, allCouplesSell, dictionary, 'SELL') for dictionary in sells]

        concurrent.futures.wait(futures)

    capital = 10000000

    num_threads = len(allCouplesBuy)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        
        futures = [executor.submit(profit_calculation, allCouplesBuy[k], allCouplesSell[k], capital) for (k, v) in allCouplesBuy.items()]

        results = [future.result() for future in futures]

    counter = 0

    for data in allCouplesBuy:
        profits.extend(results[counter])
        counter += 1
    
    profits = sorted(profits, key=lambda x: x['Profit Percentage'])
    #print(huobiSell[len(huobiSell)-2: len(huobiSell)-1])
    #print(okxSell[len(okxSell)-2: len(okxSell)-1])
    data = {}
    data['profits'] = profits
    data['bank'] = banks
    data['asset'] = allAssets
    return data #[len(profits)-2: len(profits)-1] # один самый прибильный оффер

def main():
    # fiats = ['AZN', 'AMD', 'BYN', 'KZT', 'KGS', 'MDL', 'RUB', 'TJS', 'UAH', 'TRY', 'EUR']
    fiats = ['KZT', 'RUB', 'EUR', 'USD']
    main_data = {}
    data = {}
    num_threads = len(fiats)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(parseFiat, fiat) for fiat in fiats]
        results = [future.result() for future in futures]

    counter = 0

    data['bank'] = []
    data['asset'] = []

    for fiat in fiats:
        if len(results[counter]) > 0:
            main_data[fiat] = results[counter]['profits']
            data['bank'] = list(set(data['bank'] + results[counter]['bank']))
            data['asset'] = list(set(data['asset'] + results[counter]['asset']))
            counter += 1
    data['main'] = main_data
    data['fiat'] = fiats
    data['exchange'] = ['Binance', 'OKX', 'Huobi']
    return data







if __name__ == '__main__':
    
    data = main()
    Database.insert_other(data['fiat'], 'fiat')
    Database.insert_other(data['exchange'], 'exchange')
    Database.insert_other(data['asset'], 'asset')
    Database.insert_other(data['bank'], 'bank')
    Database.insert_cryptop2p_dict(data['main'])
    asyncio.run(asyncio.sleep(10))
    
    while True:
        try:
            start_time = time.time()
            data = main()
            Database.insert_other(data['asset'], 'asset')
            Database.insert_other(data['bank'], 'bank')
            Database.insert_cryptop2p_dict(data['main'])
            print(f"Elapsed time: {time.time() - start_time} seconds\n\n")
            asyncio.run(asyncio.sleep(10))
        except psycopg2.Error as e:
            print("Error executing queries:", e)

