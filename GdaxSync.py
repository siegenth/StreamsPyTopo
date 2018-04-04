import common
import credential
from streamsx.topology.topology import *
from streamsx.topology.schema import *
from  streamsx.topology import context
from websocket import create_connection
from json import dumps, loads
import time
"""
GdaxSync - simple application that 
"""
URL = "wss://ws-feed.gdax.com"

# Descibe what you want from gdax.
params = {
    "type": "subscribe",
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD", "LTC-USD"]}]
}


def gdaxData():
    ws = create_connection(URL)
    ws.send(dumps(params))
    print("Sent")
    print("Receiving...")
    time.sleep(2)
    while True:
        yield ws.recv()

def main():
    # Sumbit request Build Server and Submit.
    schemaTicker = 'tuple<rstring type, rstring ticker, float32 price, float32 low_24h, float32 best_ask, rstring side, float32 best_bid, float34 open_24h, rstring product_id, int32 sequence, int32 trade_id, rstring time, float32 last_size, float32 volume_24h, float32 volume_30d, float32 high_24h>'
    #
    #    Define the application
    #
    topo = Topology("GdaxFeed")
    source = topo.source(gdaxData)
    source.print()
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
    test()
    #main()



