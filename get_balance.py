import numpy as np
import re

from libraries.token import Token
from libraries.global_functions import get_token_price_by_date


trading_fields = {
    "date": 0,
    "orderNro": 1,
    "pair": 2,
    "type": 3,
    "side": 4,
    "orderPrice": 5,
    "orderAmount": 6,
    "time": 7,
    "executed": 8,
    "avgPrice": 9,
    "tradingTotal": 10,
    "status": 11
}

p2p_fields = {
    "orderNro": 0,
    "orderType": 1,     # BUY or SELL
    "assetType": 2,     # Token
    "fiatType": 3,      # USD, ARS, etc
    "totalPrice": 4,    # Total 'fiatType' 
    "price": 5,         # Token price (in fiatType)
    "quantity": 6,      # Purchased token qty
    "counterparty": 7,
    "status": 8,        # Completed, etc
    "createdTime": 9    # Time (UTC)
}

STABLECOINS_NAMES = [
    "USDT",
    "BUSD",
    "DAI"
]

token_list = {}

regexName = re.compile('[^a-zA-Z]') # Only letters
regexValue = re.compile('[^\d\.]')  # Digits and point


# P2P File
with open('./reports/p2p.csv') as f:
    next(f) # Ignore first line
    for line in f:

        line = line.rstrip("\n")    # remove end of line
        values = line.split(",")

        token_name = values[p2p_fields["assetType"]]
        operated_time = values[p2p_fields["createdTime"]]
        
        if not(token_name in STABLECOINS_NAMES):
            # token_price_usd = get_token_price_by_date(token_name,operated_time)
            pass
        else:
            
            pass



# # Trading file
# with open('./reports/trading.csv') as f:
#     next(f) # Ignore first line
#     for line in f:

#         line = line.rstrip("\n") #remove end of line
#         values = line.split(",")

#         status = values[trading_fields["status"]]
#         if status=="FILLED":

#             side = values[trading_fields["side"]]
#             price = float(values[trading_fields["avgPrice"]])

#             # Split tokens and values (ex 309.6300000000USDT -> 309.63 + USDT)
#             token1_str = values[trading_fields["executed"]]
#             token1_name = regexName.sub('', token1_str)
#             token1_qty = float(regexValue.sub('', token1_str))

#             token2_str = values[trading_fields["tradingTotal"]]
#             token2_name = regexName.sub('', token2_str)
#             token2_qty = float(regexValue.sub('', token2_str))


#             if not(token2_name in STABLECOINS_NAMES):
#                 print(token2_name+" is not an stablecoin: only the balances for transactions with stablecoins are implemented")
#                 quit()
#             else:
#                 # Add new elent to token list
#                 if not(token1_name in token_list):
#                     token_list[token1_name] = Token(token1_name)

#                 token_list[token1_name].trade(side,token1_qty,price)

        
# for t in token_list.values():
#     # print("*-*-*-*")
#     print(str(t.name)+": "+str(t.get_final_qty()))
#     # print(t.purchases)
#     # print(t.sales)
#     print(" ")