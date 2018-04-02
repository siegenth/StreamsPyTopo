from streamsx.topology import context



"""
Create a service and create the Credentials, 
move them in here, needed to connect to the
service. 
"""

def build_streams_config(service_name, credentials):
    vcap_conf = {
        'streaming-analytics': [
            {
                'name': service_name,
                'credentials': credentials,
            }
        ]
    }
    trace_conf = {
        'tracing':'info',
    }

    config = {
        context.ConfigParams.VCAP_SERVICES: vcap_conf,
        context.ConfigParams.SERVICE_NAME: service_name,
        context.ConfigParams.FORCE_REMOTE_BUILD: True,
    }
    return config


