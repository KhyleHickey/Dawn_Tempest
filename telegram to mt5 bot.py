# -*- coding: utf-8 -*-
"""
Spyder Editor


"""

import MetaTrader5 as mt5
from pyrogram import Client, filters
import re
from time import sleep

path = "C:/Program Files/MetaTrader 5/terminal64.exe"
#storing channel ID of telegram trade signal group
#chat ID for telegram test group: -1001530427751
bot_token= "5608494768:AAFi4iK7sYAvPNCo2nshmb0PwqPCIZuqU5k"
channel = {-1001530427751: {'type': 'channel', 'trading': 'str_long', 'url': 'test'}}

#List of forex sysmbols
symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'GBPAUD', 'GBPCAD',
           'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
           'EURUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDCNH', 'USDJPY', 'XAUUSD']

bot = Client("KHYLE", api_id= 14045567, api_hash="45a60e6e8227f213c83904786076729c", bot_token=bot_token)

#bot.run()


def sltp(chat_id, text, Sl, Tp):
    
    try:
        if chat_id == -1001530427751:  # test
            try:
                """
                PRICE = float(re.findall(r'[\d.]+', str(text.split('\n')[0]))[0])
                SL = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Sl in i]))[-1])
                TP = float(re.findall(r'[\d.]+', str([i for i in text.split('\n') if Tp in i][-1]))[-1])
                """
                test2 = re.findall("\d+", text)
                PRICE = float(test2[0] + "." + test2[1])
                SL = float(test2[2] + "." + test2[3])
                TP = float(test2[4] + "." + test2[5])
                return [PRICE, SL, TP]
            
            except:
                return False
            print(PRICE, SL, TP)
    except Exception as ex:
        bot.send_message(-1001530427751, f"sltp.{str(chat_id)}: {ex}")
        




def OrderSend(Symbol, Lot, Type, PRICE, Sl, Tp, Magic):
    selected = mt5.symbol_select(Symbol, True)
    if not selected:
        
        bot.send_message(-1001530427751, f"OrderSend.symbol_select: {str(mt5.last_error())}")
        mt5.shutdown()
    symbol_info = mt5.symbol_info(Symbol)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Symbol,
        "volume": Lot,
        "type": Type,
        "price": PRICE,
        "sl": Sl,
        "tp": Tp,
        "deviation": 3,
        "magic": Magic,
        "comment": "Order ochish",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    #print(request, "testrun")
    print("order status is {}".format(mt5.order_check(request)))
    mt5.shutdown()
    #quit()
 
 
    

@bot.on_message(filters.text)
# @bot.on_message((filters.photo | filters.text) & (filters.channel | filters.chat))
def my_handler(client, message):
    Type = 2
    NOW_PRICE = 0
    Lot = 0.01
    chat_id = message.chat.id
    text = str(message.text).lower()
    if message.photo:
        if message.caption:
            text = message.caption
    if chat_id < 0:
        if 0 < len(text):
            if not ('limit' in text) and not ('sell stop' in text) and not ('buy stop' in text):
                if ('sl' in text and 'tp' in text) or ('stop loss' in text and 'take profit' in text):
                    for Symbol in symbols:
                        if Symbol.lower() in text:
                            #print(mt5.initialize(path), mt5.login(login=45187981, password="%3L8IQIz", server="HFMarketsGlobal-Live1"))
                            #print(mt5.initialize(path, login=45187981, server="HFMarketsGlobal-Live1", password="%3L8IQIz"))
                            if 'buy' in text:
                                Type = 0
                            if 'sell' in text:
                                Type = 1
                            st = sltp(chat_id, text, 'sl', 'tp')
                            
                            #print(st)
                            #print(mt5.initialize(login=62233926, server="MetaQuotes-Demo", password="vymsmp3g"), mt5.last_error(), abs(st[0] - mt5.symbol_info_tick("AUDUSD").bid), abs(mt5.symbol_info("AUDUSD").point))
                            #print(OrderSend(Symbol.upper(), Lot, Type, NOW_PRICE, st[1], st[2], int(str(chat_id)[-10:])))
                            
                            if st is not False and Type != 2:
                                
                                for i in range(20):
                                    if mt5.initialize(path, login=62233926, server="MetaQuotes-Demo",
                                                      password="vymsmp3g"):
                                    #if mt5.initialize(path, login=45187981, server="HFMarketsGlobal-Live1", password = "%3L8IQIz"):
                                        
                                        if mt5.symbol_info(Symbol) is not None:
                                            
                                        
                                        #if abs(st[0] - NOW_PRICE) < 200 * mt5.symbol_info(Symbol).point:
                                            print("logic true")
                                            if Type == 0:
                                                NOW_PRICE = mt5.symbol_info_tick(Symbol).ask
                                            if Type == 1:
                                                NOW_PRICE = mt5.symbol_info_tick(Symbol).bid
                                            if mt5.symbol_info(Symbol) is not None:

                                                xxx = OrderSend(Symbol.upper(), Lot, Type, NOW_PRICE, st[1], st[2],
                                                          int(str(chat_id)[-10:]))
                                                print("order check", xxx)
                                                break
                                            else:
                                                bot.send_message(-1530427751,
                                                                 f"{str(mt5.last_error())}")
                                                OrderSend(Symbol.upper(), Lot, Type, NOW_PRICE, st[1], st[2],
                                                          int(str(chat_id)[-10:]))
                                                
                                                mt5.shutdown()
                                        else:
                                            mt5.shutdown()
                                            break
                                    sleep(5)
                                    


if __name__ == "__main__":
    bot.run()

