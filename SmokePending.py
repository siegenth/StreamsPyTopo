import sys
import pickle
import common
from streamsx.topology.topology import *
from streamsx.topology.schema import *
from  streamsx.topology import context
from streamsx import rest

import streamsx.spl.op as op
import streamsx.spl.toolkit as tk

import json
import time
import argparse


def upperString(tuple):
    """Example of direct call."""
    tuple["response"] = tuple["request"].upper()
    return tuple

def lowerString(tuple):
    """Example of direct call."""
    tuple["response"] = tuple["request"].lower()
    return tuple


class webLog():
    """Example of class definition. The __init__() is executed at build time,
    on the submitters node. When it runs, the value(s) preamble are extacted
    and used.
    """
    def __init__(self, text):
        self.preamble = text + ":"

    def __call__(self, body):
        print(self.preamble, body)
        return None

def smokePending(inetToolkit, buildType, port):
    # Specify the Schema going in and out of the Streams operator.
    schemaRequest = 'tuple<int64 key, rstring request, rstring method, rstring pathInfo >'
    schemaResponse = 'tuple<int64 key, rstring request, rstring method, rstring pathInfo, rstring response >'

    topo = Topology("SmokePending")
    # Add extrenal spl functions, this is what is being testing my HTTPRequestProcess()
    tk.add_toolkit(topo, inetToolkit)
    # 'pending_source' is the loopback point.
    pending_source = PendingStream(topo)

    # Convert to Streams' tuple
    rsp = pending_source.stream.map(lambda t: t, schema=schemaResponse)

    rspFormatted = rsp.map(lambda t: json.dumps(t)).as_string()
    rspFormatted.sink(webLog("Output response"))  ## log what we have received.

    rawRequest = op.Map("com.ibm.streamsx.inet.rest::HTTPRequestProcess",
                        stream=rsp,
                        schema = schemaRequest,
                        params={'port': 8080,
                                'webTimeout': 5.0,
                                #'responseJsonAttributeName': 'string',
                                'context':'myStreams',
                                'contextResourceBase': '/base'},
                        name="TupleRequest")
    # write out data
    rawRequest.stream.sink(webLog('Input request'))  ## log what we have received.

    # determine what to work on
    # Filter does not change the type
    upperDo = rawRequest.stream.filter(lambda t: t["pathInfo"] == "/upper", name="upperFilter")
    lowerDo = rawRequest.stream.filter(lambda t: t["pathInfo"] == "/lower", name="lowerFilter")

    # do some processing
    upperDone = upperDo.map(upperString, schema = schemaResponse, name="upperProcess")
    lowerDone = lowerDo.map(lowerString, schema = schemaResponse, name="lowerProcess")
    ##
    processingDone = upperDone.union({lowerDone})

    hack = processingDone.map(lambda t: t, schema=schemaResponse)
    pending_source.complete(hack)  # close the loop
    # hack make it so I do not get this error.
    """ 
    pending_source.complete(processingDone)  # close the loop

SEVERE: Streaming Analytics service (StreamingTurbine): The submitted archive tk5385353137138356122.zip failed to build with status failed.
Exception in thread "main" java.lang.IllegalStateException: Error submitting archive for compilation:
"tk5385353137138356122/SmokePending/SmokePending.spl:5:1: CDISP0011E ERROR: A syntax error exists at the '}' token in 'graph'."
    """

    #
    #   Compile & Submit the Topology to Streams instance
    #
    streams_conf = common.build_streams_config(common.turbineName, common.turbineCredentials)
    context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate and submit ML app, data files are built with mi_build.py')
    parser.add_argument('--inetToolkit', help="Path to the INet tookit, with the new operator.",
                        default="./toolkits/streamsx.inet-master/com.ibm.streamsx.inet",
                        action='store_true')
    parser.add_argument('--port', help="Host's port the application is accepts requests on.", default="8080")
    parser.add_argument('--buildType',
                        help="Either 'DISTRIBUTED' or 'BUNDLE' determines if build+submit or just build.",
                        default="DISTRIBUTED")

    parser.add_argument('--version', action='version', version='%(prog) .5')

    args = parser.parse_args()
    print("Building the application with the following parameters:")
    print("  - inetToolkit:" + args.inetToolkit)
    print("  - buildType:" + args.buildType)
    print("  - port:" + args.port)
    smokePending(inetToolkit=args.inetToolkit, buildType=args.buildType, port=args.port)