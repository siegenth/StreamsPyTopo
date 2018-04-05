import common
import credential
import streamsx.spl.toolkit as tk
from streamsx.topology.topology import *
from streamsx.topology.schema import *
from streamsx.topology import context
from websocket import create_connection
import streamsx.spl.op as op
from json import dumps, loads
import time
import argparse

from pprint import pprint
"""
GdaxSync - simple application that 
"""
URL = "wss://ws-feed.gdax.com"

# Descibe what you want from gdax.
params = {
    "type": "subscribe",
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD", "LTC-USD"]}]
}

def scrubMessage(message):
    obj = loads(message)

    if ('type' not in obj):
        print("** No type field ")
        pprint(obj)
        print("** No type End ")
        return None
    if (obj['type'] == "subscriptions"):
        print("- Subscription Message")
        pprint(obj)
        print("- Subscription End ")
        return None
    if (obj['type'] != "ticker"):
        print("** Unknown type")
        pprint(obj)
        print("** Unknown End ")
        return None
    # All message should be ticker with full complement of fields.
    # But - in the beginning 'trade_in' is missing, sometimes.
    if "trade_id" not in obj:
        print("** Missing - trade_id field  ")
        pprint(obj)
        print("** Missing - End ")
        return None
    obj["ttype"] = obj["type"]
    del obj['type']
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
    # obj["last_size"] = float(obj["last_size"])
    # print(dumps(obj))
    return obj


def gdaxData():
    ws = create_connection(URL)
    ws.send(dumps(params))
    print("Sent")
    print("Receiving...")
    time.sleep(2)
    while True:
        scrubbed = scrubMessage(ws.recv())
        if (scrubbed is not None):
            yield scrubbed


def gdaxFeed(inetToolkit, buildType, port):
    # Sumbit request Build Server and Submit.
    schemaTicker = 'tuple<rstring ttype, float32 price, float32 low_24h, float32 best_ask, rstring side, float32 best_bid, float32 open_24h, rstring product_id, int32 sequence, int32 trade_id, rstring time, float32 last_size, float32 volume_24h, float32 volume_30d, float32 high_24h>'
    #
    #    Define the application
    #
    topo = Topology("GdaxFeed")

    tk.add_toolkit(topo, inetToolkit)

    source = topo.source(gdaxData)
    # Split out the securities : ETH-USD, LTC-USD, BTC-USD
    eth = source.filter(lambda t: t["product_id"] == "ETH-USD", name="ethFilter")
    ltc = source.filter(lambda t: t["product_id"] == "LTC-USD", name="ltcFilter")
    btc = source.filter(lambda t: t["product_id"] == "LTC-USD", name="btcFilter")
    eth.print(name="eth")
    ltc.print(name="ltc")
    btc.print(name="btc")

    ethTuple = eth.map(lambda t: t, schema=schemaTicker)
    #ethWin = ethTuple.last(datetime.timedelta(minutes=2))
    ethWin = ethTuple.last(100).trigger(1)
    rawRequest = op.Sink("com.ibm.streamsx.inet.rest::HTTPTupleView",
                        stream=ethWin,
                        params={'port': 8080,
                                'context':'gdaxLive',
                                'contextResourceBase': '/base'},
                        name="TupleView")

    #
    #   Compile & Submit the Topology to Streams instance
    #
    streams_conf = common.build_streams_config("StreamingTurbine", credential.serviceCredentials)
    context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)


def test():
    print("enter")
    tmp = gdaxData()
    while True:
        print(tmp.__next__())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build & Deploy WebSocket Stream from gdax data.')
    parser.add_argument('--inetToolkit', help="Path to the INet tookit, with the new operator.",
                        default="./toolkits/streamsx.inet-master/com.ibm.streamsx.inet",
                        action='store_true')
    parser.add_argument('--port', help="Host's port the application is accepts requests on.", default="8080")
    parser.add_argument('--buildType',
                        help="Either 'DISTRIBUTED' or 'BUNDLE' determines if scripts+submit or just scripts.",
                        default="DISTRIBUTED")
    parser.add_argument('--version', action='version', version='%(prog) .5')

    args = parser.parse_args()
    print("GDAX feed with the following parameters:")
    print("  - inetToolkit:" + args.inetToolkit)
    print("  - buildType:" + args.buildType)
    print("  - port:" + args.port)
    gdaxFeed(inetToolkit=args.inetToolkit, buildType=args.buildType, port=args.port)




