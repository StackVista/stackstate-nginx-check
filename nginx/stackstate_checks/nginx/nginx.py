# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
import crossplane
import uuid


class Http():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.virtual_servers = {}


class VirtualServer():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.locations = {}


class Location():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.servers = {}


class Server():
    def __init__(self):
        self.name = ""


class NginxCheck(AgentCheck):
    INSTANCE_TYPE = "nginx"
    SERVICE_CHECK_NAME = "Nginx"

    def __init__(self, name, init_config, instances=None):
        AgentCheck.__init__(self, name, init_config, instances)
        self.payload = None
        self.name = None
        self.http = None

    def get_instance_key(self, instance):
        if "name" not in instance:
            raise ConfigurationError("Missing name in topology instance configuration.")
        if "location" not in instance:
            raise ConfigurationError("Missing location in topology instance configuration.")

        location = instance["location"]
        return TopologyInstance(self.INSTANCE_TYPE, location)

    def check(self, instance):
        name, location = self._get_config(instance)
        self.name = name
        self.start_snapshot()
        try:
            self.log.info("Processing file: {file}".format(file=location))
            self.payload = crossplane.parse(location)
            self._parse_topology()
            self._create_topology()
        except Exception as err:
            msg = "Nginx check failed: {}".format(str(err))
            self.log.error(msg)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=msg, tags=[])
        finally:
            self.stop_snapshot()

    def _get_config(self, instance):
        return (instance["name"], instance["location"])

    def _parse_topology(self):
        if self.payload['status'] != "ok" or len(self.payload["errors"]) > 0:
            raise "incorrect payload"
        if len(self.payload['config']) > 0:
            self._process_config(self.payload['config'][0])

    def _process_config(self, config, parent_id=None):
        self.log.debug("Processing config: {}".format(config['file']))
        if config['status'] != "ok" or len(config['errors']) > 0:
            raise "incorrect payload config: {file}".format(file=config['file'])
        for parsed in config['parsed']:
            self._process_parsed(parsed, parent_id)

    def _process_parsed(self, parsed, parent_id):
        id = str(uuid.uuid4())
        self.log.debug("Processing id: {}".format(id))
        if parsed['directive'] == 'http':
            external_id = "urn:nginx:http:{}".format(self.name)
            self.http = Http(id=id, external_id=external_id)
        if parsed['directive'] == 'server':
            self.log.error("Processing directive server for {}".format(id))
            external_id = "urn:nginx:server:{}:{}".format(self.name, "unknown")
            self.http.virtual_servers[id] = VirtualServer(id=id, external_id=external_id)
        if parsed['directive'] == 'listen':
            external_id = "urn:nginx:server:{}:{}".format(self.name, ":".join(parsed['args']))
            self.http.virtual_servers[parent_id].external_id = external_id
        if parsed['directive'] == 'location':
            external_id = "urn:nginx:location:{}:{}".format(self.name, ":".join(parsed['args']))
            self.http.virtual_servers[parent_id].locations[id] = Location(id=id, external_id=external_id)
        self.log.debug("Done processing id: {}".format(id))
        if 'block' in parsed:
            for block in parsed['block']:
                if block['directive'] == "include":
                    for include in block['includes']:
                        self._process_config(self.payload['config'][include], parent_id=id)
                else:
                    self._process_parsed(block, parent_id=id)

    def _create_topology(self):
        if self.http:
            self.log.debug("Creating component: {}".format(self.http.external_id))
            self.component(self.http.external_id, "nginx_http", {})
            for vs_id, virtual_server in self.http.virtual_servers.items():
                self.log.debug("Creating component: {}".format(virtual_server.external_id))
                self.component(virtual_server.external_id, "nginx_virtual_server", {})
                self.relation(self.http.external_id, virtual_server.external_id, "has", {})
                for l_id, location in virtual_server.locations.items():
                    self.component(location.external_id, "nginx_location", {})
                    self.relation(virtual_server.external_id, location.external_id, "has", {})
