# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
from urllib.parse import urlparse
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
        self.proxy_pass = None
        # The upstream servers (in case of proxy_pass directive)
        self.servers = {}


# Corresponds with an upstream server
class Server():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id


class NginxCheck(AgentCheck):
    INSTANCE_TYPE = "nginx"
    SERVICE_CHECK_NAME = "Nginx"

    def __init__(self, name, init_config, instances=None):
        AgentCheck.__init__(self, name, init_config, instances)
        self.payload = None
        self.name = None
        self.http = None
        self.upstreams = {}

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
            self._parse_upstreams()
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

    def _process_config(self, config, parent=None):
        self.log.debug("Processing config: {}".format(config['file']))
        if config['status'] != "ok" or len(config['errors']) > 0:
            raise "incorrect payload config: {file}".format(file=config['file'])
        for parsed in config['parsed']:
            self._process_parsed(parsed, parent)

    def _process_parsed(self, parsed, parent):
        id = str(uuid.uuid4())
        new_parent = None
        self.log.debug("Processing id: {}".format(id))
        if parsed['directive'] == 'http':
            external_id = "urn:nginx:http:{}".format(self.name)
            self.http = Http(id=id, external_id=external_id)
            new_parent = self.http
        if parsed['directive'] == 'server':
            self.log.debug("Processing directive server for {}".format(id))
            external_id = "urn:nginx:server:{}:{}".format(self.name, "unknown")
            parent.virtual_servers[id] = VirtualServer(id=id, external_id=external_id)
            new_parent = parent.virtual_servers[id]
        if parsed['directive'] == 'listen':
            external_id = "urn:nginx:server:{}:{}".format(self.name, ":".join(parsed['args']))
            parent.external_id = external_id
        if parsed['directive'] == 'location':
            external_id = "urn:nginx:location:{}:{}".format(self.name, ":".join(parsed['args']))
            parent.locations[id] = Location(id=id, external_id=external_id)
            new_parent = parent.locations[id]
        if parsed['directive'] == 'proxy_pass':
            parent.proxy_pass = parsed['args'][0]
        if parsed['directive'] == 'upstream':
            # An upstream directive should be parsed later, when the proxy_pass / location directives have been parsed.
            self.upstreams[parsed['args'][0]] = parsed
            return
        self.log.debug("Done processing id: {}".format(id))
        if 'block' in parsed:
            for block in parsed['block']:
                if block['directive'] == "include":
                    for include in block['includes']:
                        self._process_config(self.payload['config'][include], parent=new_parent)
                else:
                    self._process_parsed(block, parent=new_parent)

    def _parse_upstreams(self):
        for vkey, vserver in self.http.virtual_servers.items():
            for lkey, location in vserver.locations.items():
                if location.proxy_pass:
                    self._process_upstream(location)

    def _process_upstream(self, location):
        self.log.error("Processing upstream {}".format(location.proxy_pass))
        parsed = self.upstreams[urlparse(location.proxy_pass).netloc]
        for server in parsed['block']:
            id = str(uuid.uuid4())
            external_id = "urn:nginx:upstream:{}:{}".format(self.name, ":".join(server['args']))
            location.servers[id] = Server(id, external_id)

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
                    for s_id, server in location.servers.items():
                        self.component(server.external_id, "nginx_upstream_server", {})
                        self.relation(location.external_id, server.external_id, "has", {})
