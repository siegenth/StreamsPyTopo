from sseclient import SSEClient as EventSource
import common
import credential
import streamsx.spl.toolkit as tk
from streamsx.topology.topology import *
from streamsx.topology.schema import *
from streamsx.topology import context
from websocket import create_connection
import streamsx.spl.op as op
import argparse


def wikiStream():
    url = 'https://stream.wikimedia.org/v2/stream/recentchange'
    for event in EventSource(url):
        """Thie fields that are specified by SSE: event, data, id, retry """
        if event.event == 'message':
            try:
                changeData = json.loads(event.data)
                if changeData.get("length") is None:
                    old = 0
                    new = 0
                else:
                    try:
                        old = int(changeData["length"]["old"])
                    except ValueError:
                        old = 0
                    except TypeError:
                        old = 0
                    try:
                        new = int(changeData["length"]["new"])
                    except ValueError:
                        new = 0
                    except TypeError:
                        new = 0
                yield {'dataId':changeData["id"],
                       'bot':changeData["bot"],
                       'domain':changeData["meta"]["domain"],
                       'lenOld':old,
                       'lenNew':new,
                       'SSEid': event.id,
                       'SSEdata': event.data,
                       'SSEevent': event.event
                       }
            except ValueError:
                pass
        else:
            pass
            #print('{user} edited {title}'.format(**change))


#url = "https://proxy.streamdata.io/http://stockmarket.streamdata.io/prices/"



def wikiFeed(inetToolkit, buildType, port):
    # Sumbit request Build Server and Submit.
    schemaTicker = 'tuple<rstring dataId, rstring bot, rstring domain, int32 lenOld,int32 lenNew, rstring SSEdata, rstring SSEevent>'
    #
    #    Define the application
    #
    topo = Topology("WikiFeed")

    tk.add_toolkit(topo, inetToolkit)

    source = topo.source(wikiStream)
    # Only one type of event, verity that I got it right.
    event = source.filter(lambda t: t["SSEevent"] == "message", name="eventFilter")
    event.print(name="eth")

    eventTuple = event.map(lambda t: t, schema=schemaTicker)
    eventWin = eventTuple.last(100).trigger(1)
    rawRequest = op.Sink("com.ibm.streamsx.inet.rest::HTTPTupleView",
                        stream=eventWin,
                        params={'port': 8081,
                                'context':'gdaxEth',
                                'contextResourceBase': '/base'},
                        name="TupleView")

    #
    #   Compile & Submit the Topology to Streams instance
    #
    streams_conf = common.build_streams_config("StreamingTurbine", credential.serviceCredentials)
    context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)

if __name__ == '__test__':
    tmp = wikiStream(url)
    while True:
        print(tmp.__next__())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build & Deploy WebSocket Stream from gdax data.')
    parser.add_argument('--inetToolkit', help="Path to the INet tookit, with the new operator.",
                        default="./toolkits/streamsx.inet-master/com.ibm.streamsx.inet",
                        action='store_true')
    parser.add_argument('--port', help="Host's port the application is accepts requests on.", default="8081")
    parser.add_argument('--buildType',
                        help="Either 'DISTRIBUTED' or 'BUNDLE' determines if scripts+submit or just scripts.",
                        default="DISTRIBUTED")
    parser.add_argument('--version', action='version', version='%(prog) .5')

    args = parser.parse_args()
    print("GDAX feed with the following parameters:")
    print("  - inetToolkit:" + args.inetToolkit)
    print("  - buildType:" + args.buildType)
    print("  - port:" + args.port)
    wikiFeed(inetToolkit=args.inetToolkit, buildType=args.buildType, port=args.port)

