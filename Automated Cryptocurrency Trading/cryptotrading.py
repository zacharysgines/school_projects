api_key = 'PKOOIPO3M4O7RKE7PC4KKPQQAI'
secret_key = '7pr9gAAuRuxkW32CAkzRY9sGikyfRvs2BPwvzousr3oK'

import requests
from alpaca.trading.client import TradingClient
import json
import networkx as nx
import os
from datetime import datetime
import time

# Initialize Alpaca trading client
trading_client = TradingClient(api_key, secret_key, paper=True)

# ----- Create graph -----
g = nx.DiGraph()

# Load API data
url = ('https://api.coingecko.com/api/v3/simple/price?ids='
       'ethereum,bitcoin,litecoin,ripple,cardano,bitcoin-cash,eos&'
       'vs_currencies=eth,btc,ltc,xrp,ada,bch,eos')

trading_url = "https://paper-api.alpaca.markets/v2/orders"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key
}

response = requests.get(url)
prices = response.json()

# Mapping for each coin and its ID
code_map = {
    'bitcoin': 'btc', 'btc': 'bitcoin',
    'ethereum': 'eth', 'eth': 'ethereum',
    'litecoin': 'ltc', 'ltc': 'litecoin',
    'ripple': 'xrp', 'xrp': 'ripple',
    'cardano': 'ada', 'ada': 'cardano',
    'bitcoin-cash': 'bch', 'bch': 'bitcoin-cash',
    'eos': 'eos'
}

# Create folder to hold currency pair files
os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y.%m.%d:%H.%M")
filename = f"data/currency_pair_{timestamp}.txt"

with open(filename, "w") as f:
    f.write("currency_from,currency_to,exchange_rate\n")

    # Create graph edges and save to file
    for base_id_full, sub_currency in prices.items():
        base_id = code_map[base_id_full]
        for sub_id, rate in sub_currency.items():
            if base_id != sub_id and not g.has_edge(base_id, sub_id):
                try:
                    sub_currency_full = code_map[sub_id]
                    reverse_rate = prices[sub_currency_full][base_id]
                    g.add_weighted_edges_from([
                        (base_id, sub_id, rate),
                        (sub_id, base_id, reverse_rate)
                    ])
                    f.write(f"{base_id},{sub_id},{rate}\n")
                    f.write(f"{sub_id},{base_id},{reverse_rate}\n")
                except:
                    continue

nodes = g.nodes

# Helper function to place order safely
def place_order(symbol, side, qty=None, notional=None, max_wait=15):
    payload = {
        "type": "market",
        "time_in_force": "gtc",
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "notional": str(notional) if notional else None
    }
    try:
        response = requests.post(trading_url, json=payload, headers=headers, timeout=10)
        order = response.json()
    except Exception as e:
        print(f"Order placement failed for {symbol}: {e}")
        return None

    order_id = order.get('id')
    if not order_id:
        print(f"No order ID returned for {symbol}. Skipping.")
        return None

    # Wait until order is filled or timeout
    start_time = time.time()
    while True:
        try:
            status_resp = requests.get(f"{trading_url}/{order_id}", headers=headers, timeout=10)
            order_status = status_resp.json()
        except Exception as e:
            print(f"Error checking order status for {symbol}: {e}")
            return None

        if order_status.get('status') == 'filled':
            return order_status
        elif time.time() - start_time > max_wait:
            print(f"Order for {symbol} not filled after {max_wait}s. Skipping.")
            return None
        else:
            time.sleep(1)

# Main loop for path evaluation
for node1 in nodes:
    for node2 in nodes:
        if node1 == node2:
            continue

        paths = nx.all_simple_paths(g, node1, node2)
        for path in paths:
            weight = 1.0
            reverse_weight = 1.0

            # Forward weight
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                weight *= g[u][v]['weight']

            # Reverse weight
            for i in range(len(path) - 1, 0, -1):
                u, v = path[i], path[i-1]
                reverse_weight *= g[u][v]['weight']

            path_balance = weight * reverse_weight

            if path_balance > 1:
                full_path = path + path[-2::-1]
                amount_usd = 50

                for i in range(len(full_path) - 1):
                    current_coin = full_path[i].upper() + "USD"
                    next_coin = full_path[i + 1].upper() + "USD"

                    if amount_usd < 1:  # Skip tiny amounts
                        print("Amount too small to buy, skipping leg.")
                        break

                    print(f"Starting buy: {current_coin} with ${amount_usd}")
                    buy_order = place_order(current_coin, "buy", notional=amount_usd)
                    if not buy_order:
                        break

                    qty_current_coin = float(buy_order.get('filled_qty', 0))
                    print("Buy filled:", buy_order)

                    print(f"Starting sell: {current_coin} to {next_coin}")
                    sell_order = place_order(current_coin, "sell", qty=qty_current_coin)
                    if not sell_order:
                        break

                    amount_usd = float(sell_order['filled_avg_price']) * float(sell_order['filled_qty'])
                    print("Sell filled:", sell_order)

                    time.sleep(0.5)  # Slight delay between legs
