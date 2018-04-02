from websocket import WebSocketApp
from json import dumps, loads
from pprint import pprint
# pip install websocket-client

URL = "wss://ws-feed.gdax.com"
msgCount = 0
fo = None
def on_message(_, message):
    global msgCount
    """Callback executed when a message comes.
    Positional argument:
    message -- The message itself (string)
    """
    obj = loads(message)
    #pprint(obj)


    if ('type' not in obj):
        print("** No type field ")
        pprint(obj)
        print("** No type End ")
        return
    if (obj['type'] == "subscriptions"):
        print("- Subscription Message")
        pprint(obj)
        print("- Subscription End ")
        return
    if (obj['type'] != "ticker"):
        print("** Unknown type")
        pprint(obj)
        print("** Unknown End ")
        return
    # All message should be ticker with full complement of fields.
    # But - in the beginning 'trade_in' is missing, sometimes.
    if "trade_id" not in  obj:
        print("** Missing - trade_id field  ")
        pprint(obj)
        print("** Missing - End ")
        return
    obj["sequence"] = int(obj["sequence"])
    obj["trade_id"] = int(obj["trade_id"])
    obj["price"] = float(obj["price"])
    obj["best_ask"] = float(obj["best_ask"])
    obj["best_bid"] = float(obj["best_bid"])
    obj["open_24h"] = float(obj["open_24h"])
    obj["low_24h"] = float(obj["low_24h"])
    obj["high_24h"] = float(obj["high_24h"])
    obj["volume_24h"] = float(obj["volume_24h"])
    obj["volume_30d"] = float(obj["volume_30d"])
    obj["last_size"] = float(obj["last_size"])
    #obj["last_size"] = float(obj["last_size"])
    #print(dumps(obj))
    fo.write(dumps(obj) + ",\n")
    fo.flush()
    msgCount += 1
    if msgCount > 10:
        exit(0)
    print("**** MessageCount: %s" % str(msgCount))

def on_open(socket):
    """Callback executed at socket opening.
    Keyword argument:
    socket -- The websocket itself
    """
    global fo
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD", "LTC-USD"]}]
    }
    fo = open("archive/gdax.json", "w")
    socket.send(dumps(params))


def main():
    """Main function."""
    ws = WebSocketApp(URL, on_open=on_open, on_message=on_message)
    ws.run_forever()

if __name__ == '__main__':
    main()
