# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import crossplane
import traceback
import uuid


class ConfigError(Exception):
    """Basic exception for when nginx json payload contains errors"""


class Http():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.virtual_servers = {}

    # Create Http component in stackstate
    def create_http(self, nginx_topo):
        nginx_topo.log.debug("Creating component: {}".format(self.external_id))
        http_data = {"layer": "HTTP"}
        http_data["domain"] = "{}".format(nginx_topo.name)
        http_data["name"] = "http"
        nginx_topo.component(self.external_id, "nginx_http", http_data)
        for vs_id, virtual_server in self.virtual_servers.items():
            virtual_server.create_virtual_server(self, nginx_topo)


class VirtualServer():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.listen = None
        self.status_zone = None
        self.locations = {}

    # Create virtual server in stackstate
    def create_virtual_server(self, http, nginx_topo):
        nginx_topo.log.debug("Creating component: {}".format(self.external_id))
        server_data = {"layer": "Virtual Server"}
        server_data["domain"] = "{}".format(nginx_topo.name)
        server_data["name"] = "{}".format(self.listen)
        if self.status_zone:
            server_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.component(self.external_id, "nginx_virtual_server", server_data)
        nginx_topo.relation(http.external_id, self.external_id, "has", {})
        for l_id, location in self.locations.items():
            location.create_location(self, nginx_topo)


class Location():
    def __init__(self, id, external_id, location_name):
        self.id = id
        self.external_id = external_id
        self.location_name = location_name
        self.status_zone = None
        # The upstream servers
        self.proxy_pass = None  # String representing the proxy value
        self.upstream = None  # Actual proxy pass upstream object

    # Create location in stackstate
    def create_location(self, virtual_server, nginx_topo):
        location_data = {"layer": "Location"}
        location_data["domain"] = "{}".format(nginx_topo.name)
        location_data["name"] = "{}".format(self.location_name)
        if self.status_zone:
            location_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.log.debug("Location id: {} - data: {}".format(self.external_id, location_data))
        nginx_topo.component(self.external_id, "nginx_location", location_data)
        nginx_topo.relation(virtual_server.external_id, self.external_id, "has", {})
        if self.upstream:
            self.upstream.create_upstream(self, nginx_topo)


class Upstream():
    def __init__(self, id, external_id):
        self.id = id
        self.external_id = external_id
        self.upstream_name = None
        self.status_zone = None
        # The upstream servers
        self.servers = {}

    # Create upstream in stackstate
    def create_upstream(self, location, nginx_topo):
        upstream_data = {"layer": "Upstream"}
        upstream_data["domain"] = "{}".format(nginx_topo.name)
        upstream_data["name"] = "{}".format(self.upstream_name)
        if self.status_zone:
            upstream_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.component(self.external_id, "nginx_upstream", upstream_data)
        nginx_topo.relation(location.external_id, self.external_id, "has", {})
        for s_id, server in self.servers.items():
            server.create_server(self, nginx_topo)


# Corresponds with an upstream server
class Server():
    def __init__(self, id, external_id, server_name):
        self.id = id
        self.external_id = external_id
        self.server_name = server_name

    # Create upstream server in stackstate
    def create_server(self, upstream, nginx_topo):
        upstream_server_data = {"layer": "Upstream Server"}
        upstream_server_data["domain"] = "{}".format(nginx_topo.name)
        upstream_server_data["name"] = "{}".format(self.server_name)
        upstream_server_data["upstream"] = "{}".format(upstream.upstream_name)
        nginx_topo.component(self.external_id, "nginx_upstream_server", upstream_server_data)
        nginx_topo.relation(upstream.external_id, self.external_id, "has", {})


class NginxTopo(AgentCheck):
    INSTANCE_TYPE = "nginx"
    SERVICE_CHECK_NAME = "NginxTopo"

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

        name = instance["name"]
        return TopologyInstance(self.INSTANCE_TYPE, name)

    def check(self, instance):
        name, location = self._get_config(instance)
        self.name = name
        self.start_snapshot()
        try:
            self.log.debug("Processing file: {file}".format(file=location))
            self.payload = crossplane.parse(location)
            self._parse_topology()
            self._parse_upstreams()
            self._create_topology()
        except Exception as err:
            msg = "Nginx check failed: {}".format(str(err))
            self.log.error(traceback.format_exc())
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=msg, tags=[])
        finally:
            self.stop_snapshot()

    def _get_config(self, instance):
        return (instance["name"], instance["location"])

    def _parse_topology(self):
        if self.payload['status'] != "ok" or len(self.payload["errors"]) > 0:
            raise ConfigError("Incorrect payload: {status} - {errors}"
                              .format(status=self.payload['status'],
                                      errors="|".join(error['error'] for error in self.payload['errors'])))
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
            external_id = "urn:nginx:{}:http".format(self.name)
            self.http = Http(id=id, external_id=external_id)
            new_parent = self.http
        if parsed['directive'] == 'server':
            self.log.debug("Processing directive server for {}".format(id))
            external_id = "urn:nginx:{}:server:{}".format(self.name, "unknown")
            parent.virtual_servers[id] = VirtualServer(id=id, external_id=external_id)
            new_parent = parent.virtual_servers[id]
        if parsed['directive'] == 'listen':
            parent.listen = ":".join(parsed['args'])
            external_id = "urn:nginx:{}:server:{}".format(self.name, parent.listen)
            parent.external_id = external_id
        if parsed['directive'] == 'status_zone':
            parent.status_zone = parsed['args'][0]
        if parsed['directive'] == 'location':
            location_name = ":".join(parsed['args'])
            external_id = "urn:nginx:{}:server:{}:location:{}".format(self.name, parent.listen,
                                                                      location_name)
            parent.locations[id] = Location(id=id, external_id=external_id, location_name=location_name)
            new_parent = parent.locations[id]
        if parsed['directive'] == 'proxy_pass':
            parent.proxy_pass = parsed['args'][0]
        if parsed['directive'] == 'upstream':
            # An upstream directive should be parsed later, when the proxy_pass / location directives have been parsed.
            self.upstreams[parsed['args'][0]] = parsed
            return
        if parsed['directive'] == 'include':
            for include in parsed['includes']:
                self._process_config(self.payload['config'][include], parent=parent)
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
        self.log.debug("Processing upstream {}".format(location.proxy_pass))
        upstream_name = urlparse(location.proxy_pass).netloc
        parsed = self.upstreams[upstream_name]
        upstream_id = str(uuid.uuid4())
        upstream_ext_id = "urn:nginx:{}:upstream:{}".format(self.name, upstream_name)
        location.upstream = Upstream(upstream_id, upstream_ext_id)
        location.upstream.upstream_name = upstream_name
        for block in parsed['block']:
            if block['directive'] == 'server':
                server_id = str(uuid.uuid4())
                server_name = ":".join(block['args'])
                server_external_id = "urn:nginx:{}:upstream:{}:server:{}".format(self.name,
                                                                                 upstream_name,
                                                                                 server_name)
                location.upstream.servers[server_id] = Server(server_id, server_external_id, server_name)
            if block['directive'] == 'zone':
                location.upstream.status_zone = block['args'][0]

    def _create_topology(self):
        if self.http:
            self.http.create_http(self)
