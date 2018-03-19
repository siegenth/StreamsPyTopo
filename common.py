from streamsx.topology import context


creds = {"rest_port": "443",
         "password": "75b6123b-bca2-408a-a89b-bba52588b594",
         "bundles_path": "/jax-rs/bundles/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "resources_path": "/jax-rs/resources/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "stop_path": "/jax-rs/streams/stop/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "rest_host": "streams-app-service.ng.bluemix.net",
         "size_path": "/jax-rs/streams/size/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "jobs_path": "/jax-rs/jobs/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "start_path":
             "/jax-rs/streams/start/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50",
         "rest_url":
             "https://streams-app-service.ng.bluemix.net", "userid": "5f6be447-e9bc-4f0d-9f44-66f380ba6e13",
         "status_path": "/jax-rs/streams/status/service_instances/adcbc82c-aa84-42d5-9e33-26bad08cac55/service_bindings/1b93190c-da0e-4ae5-a45b-851e9e047c50"}

"""
Create a service and create the Credentials, 
move them in here, needed to connect to the
service. 
"""

"""
turbineCredentials = {
  "apikey": "1dNgWPMeLtS6PndZMFdP6qY4NiL9HixnFLetpJt1r2Nn",
  "bundles_path": "/jax-rs/bundles/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:streaming-analytics:us-south:a/309e3606a35c9fea12981876cd991b07:30b4f155-7348-4836-a120-bf7608ac5c7d::",
  "iam_apikey_name": "auto-generated-apikey-35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/309e3606a35c9fea12981876cd991b07::serviceid:ServiceId-3df675d8-3637-4405-a5d4-f598453b94e6",
  "jobs_path": "/jax-rs/jobs/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "password": "5e363f94-e60b-45ed-b8ce-19b8b2acb450",
  "resources_path": "/jax-rs/resources/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "rest_host": "streams-app-service.ng.bluemix.net",
  "rest_port": "443",
  "rest_url": "https://streams-app-service.ng.bluemix.net",
  "size_path": "/jax-rs/streams/size/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "start_path": "/jax-rs/streams/start/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "status_path": "/jax-rs/streams/status/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "stop_path": "/jax-rs/streams/stop/service_instances/30b4f155-7348-4836-a120-bf7608ac5c7d/service_bindings/35ba6f38-d2eb-4f53-a2be-63178a4fda86",
  "userid": "f29a0fb2-3fd5-40b4-b3fb-16bc02b40d9b",
  "v2_rest_url": "https://streams-app-service.ng.bluemix.net/v2/streaming_analytics/30b4f155-7348-4836-a120-bf7608ac5c7d"
}
TurbineDefinition = [turbineName, turbineCredentials]
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


