from pybit.unified_trading import HTTP
import time
import math
session = HTTP(
    testnet=False,
    api_key="",
    api_secret="",
)

def value(price, balance):
    amount = float(balance)/float(price)
    formatted_float = math.floor(amount * 10**2) / 10**2
    return formatted_float

print(session.get_spot_asset_info())


def get_balance():
    coins=session.get_wallet_balance(accountType="unified")['result']['list'][0]['coin']
    balance=0
    for coin in coins:
        if coin['coin']=="USDT":
            balance=coin['walletBalance']
    return float(balance)

def buy():
    coins=session.get_wallet_balance(accountType="unified")['result']['list'][0]['coin']

    balance=0
    for coin in coins:
        if coin['coin']=="USDT":
            balance=coin['walletBalance']
    print(balance)

    price_to_buy=session.get_tickers(category="linear", symbol="ADAUSDT")['result']['list'][0]['lastPrice']
    price_to_buy=math.floor(float(price_to_buy) * 10**2) / 10**2
    amount_to_buy=value(price_to_buy,balance)
    temp=False
    try:
        order=session.place_order( category="spot",
            symbol="ADAUSDT",
            side="Buy",
            orderType="Limit",
            qty=amount_to_buy,
            price=price_to_buy,
            isLeverage=0,
            orderFilter="Order",)
        print(order)
        temp=True
    except Exception as e:
        print(e)
        if "Insufficient" in str(e):
            o=session.cancel_all_orders(category="spot")
            print(o)

        

    price_to_sell=float(price_to_buy)+0.02
    return price_to_sell,temp

flag="yes"

price_to_sell,t=buy()
#amount_to_sell=0.0154

def value_to_sell():
    coins=session.get_wallet_balance(accountType="unified")['result']['list'][0]['coin']
    balance=0
    for coin in coins:
        if coin['coin']=="ADA":
            balance=coin['walletBalance']
    balance=math.floor(float(balance) * 10**2) / 10**2
    return balance
amount_to_sell=value_to_sell()
amount_to_sell = math.floor(float(amount_to_sell) * 10**2) / 10**2 
bigcnt=0
sel=0
while True:
    price=session.get_tickers(category="linear", symbol="ADAUSDT")['result']['list'][0]['lastPrice']
    print("I am in part 1")
    if float(price)>price_to_sell:
        bigcnt=0
        
        #price2=session.get_tickers(category="linear", symbol="ADAUSDT")['result']['list'][0]['lastPrice']
        #price2=float(price2)
        #price = float(price)
        #while price2 > price:
        #    price2=session.get_tickers(category="linear", symbol="ADAUSDT")['result']['list'][0]['lastPrice']
        #time.sleep(0.0001)
        

        #if float(price2)>price_to_sell:
        price_to_sell=session.get_tickers(category="linear", symbol="ADAUSDT")['result']['list'][0]['lastPrice']
        price_to_sell=math.floor(float(price_to_sell) * 10**2) / 10**2
        price=math.floor(float(price) * 10**2) / 10**2

        #session.place_order(category="spot",symbol="ADAUSDT",side="Buy",orderType="Limit",qty=amount_to_buy,price=price_to_buy,timeInForce="PostOnly",orderLinkId="spot-test-postonly",isLeverage=0,orderFilter="Order",)
        print(flag)
        amount_to_sell=value_to_sell()
        order="order is going to occur"
        print(order)
        try:
            order=session.place_order( category="spot", symbol="ADAUSDT", side="SELL", orderType="Limit", qty=amount_to_sell, price=price,isLeverage=0, orderFilter="Order",)
        except Exception as e:
            print(e)
        time.sleep(600)
        print(order)
        print("I am in part 5")
        price_to_sell,temp=buy()
        cnt=0
        balance=get_balance()
        while temp == False:
            print("I am in part 3")

            price_to_sell,temp=buy()
            cnt+=1
            if cnt>10:
                o=session.cancel_all_orders(category="spot")
                print(o)
                temp=True
            time.sleep(1)
    if bigcnt>60:
        price_to,t=buy()
        bigcnt=0
        if sel>10000:
            price_to_sell,t=buy()
            sel=0
    bigcnt+=1
    sel+=1
    time.sleep(1)


