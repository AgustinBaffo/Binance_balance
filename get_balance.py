import os
import numpy as np
import pickle
import re
import hashlib

from libraries.token import Token
from libraries.global_functions import get_token_price_by_date


REPORT_TRADING_PATH = './reports/trading.csv'
REPORT_P2P_PATH = './reports/p2p.csv'
P2P_DATA_PATH = './data/p2p_report.pickle'
P2P_HASH_PATH = './data/p2p_hash.pickle'

use_previous_data_p2p_data = True


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

regexName = re.compile('[^a-zA-Z]')     # Only letters
regexValue = re.compile('[^\d\.]')      # Digits and point
regexRemoveComma = re.compile(r'(?!(([^"]*"){2})*[^"]*$),') # Commas between quotes marks

def get_hash_file(file_path):
    with open(file_path, 'rb') as f:  # opened in binary mode!
        hash_value = hashlib.md5(f.read()).hexdigest()
    return hash_value


####################################
## Read p2p file.
####################################

# If file was already read, the data was already downloaded and storaged and the file wasn't change => use previous data
need_read_p2p_file = True

# Check if previous file information exist
if use_previous_data_p2p_data and os.path.exists(P2P_DATA_PATH) and os.path.exists(P2P_HASH_PATH):

    # Load previous hash from pickle and get hash from new file
    with open(P2P_HASH_PATH, 'rb') as handle:
        prev_hash_value = pickle.load(handle)
    
    new_hash_value = get_hash_file(REPORT_P2P_PATH)

    if new_hash_value == prev_hash_value: # File didn't change
        
        print("P2P report didn't change: using previous data")

        # Load p2p data from pickle
        print("Load p2p datafrom "+str(P2P_DATA_PATH))
        with open(P2P_DATA_PATH, 'rb') as handle:
            token_list = pickle.load(handle)

        need_read_p2p_file = False

if need_read_p2p_file:

    print("Reading P2P report")

    # P2P File
    with open(REPORT_P2P_PATH) as f:
        next(f) # Ignore first line
        for line in f:

            line = line.rstrip("\n")    # remove end of line
            values = line.split(",")

            status = values[p2p_fields["status"]]

            if status=="Completed":

                token_name = values[p2p_fields["assetType"]]
                token_qty = float(values[p2p_fields["quantity"]])
                operated_time = values[p2p_fields["createdTime"]]
                side = values[p2p_fields["orderType"]]
                
                if not(token_name in STABLECOINS_NAMES):
                    token_price_usd = get_token_price_by_date(token_name,operated_time)

                    # Add new elent to token list
                    if not(token_name in token_list):
                        token_list[token_name] = Token(token_name)

                    token_list[token_name].trade(side,token_qty,token_price_usd)

    # Save data into pickle
    with open(P2P_DATA_PATH, 'wb') as handle:
        pickle.dump(token_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # Save hash into pickle
    new_hash_value = get_hash_file(REPORT_P2P_PATH)
    with open(P2P_HASH_PATH, 'wb') as handle:
        pickle.dump(new_hash_value, handle, protocol=pickle.HIGHEST_PROTOCOL)


####################################
## Read trading file.
####################################

print("Reading trading report")
with open(REPORT_TRADING_PATH) as f:
    next(f) # Ignore first line
    for line in f:

        line = line.rstrip("\n")                # remove end of line
        line = regexRemoveComma.sub('', line)   # remove comma between quotes
        line = line.replace('"', "")                   # remove quotes

        values = line.split(",")
        status = values[trading_fields["status"]]

        if status=="FILLED":
            side = values[trading_fields["side"]]
            price = float(values[trading_fields["avgPrice"]])

            # Split tokens and values (ex 309.6300000000USDT -> 309.63 + USDT)
            token1_str = values[trading_fields["executed"]]
            token1_name = regexName.sub('', token1_str)
            token1_qty = float(regexValue.sub('', token1_str))

            token2_str = values[trading_fields["tradingTotal"]]
            token2_name = regexName.sub('', token2_str)
            token2_qty = float(regexValue.sub('', token2_str))


            if not(token2_name in STABLECOINS_NAMES):
                print(token2_name+" is not an stablecoin: only the balances for transactions with stablecoins are implemented")
                quit()
            else:

                # Add new elent to token list
                if not(token1_name in token_list):
                    token_list[token1_name] = Token(token1_name)

                token_list[token1_name].trade(side,token1_qty,price)

        
for t in token_list.values():
    print("\n\n*-*-*-*-*")
    print(str(t.name)+":")
    t.compile()
    print("Held token quantity: "+str(t.get_final_qty()))
    print("Earns: "+str(t.get_earns()))