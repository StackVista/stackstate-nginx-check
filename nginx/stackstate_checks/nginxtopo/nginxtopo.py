# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import crossplane
import os
import traceback
import uuid


class ConfigError(Exception):
    """Basic exception for when nginx json payload contains errors"""


class Topo():
    def __init__(self, id, external_id, filename, line):
        self.id = id
        self.external_id = external_id
        self.filename = filename
        self.line = line

    def initialize_data(self, nginx_topo, layer, name):
        nginx_topo.log.debug("Creating component: {}".format(self.external_id))
        data = {"layer": "{}".format(layer)}
        data["domain"] = "{}".format(nginx_topo.name)
        data["name"] = "{}".format(name)
        if nginx_topo.baseurl:
            data["scm"] = "{baseurl}{filename}#L{line}".format(baseurl=nginx_topo.baseurl, filename=self.filename,
                                                               line=self.line)
        return data


class Http(Topo):
    def __init__(self, id, external_id, filename, line):
        Topo.__init__(self, id, external_id, filename, line)
        self.virtual_servers = {}

    # Create Http component in stackstate
    def create_http(self, nginx_topo):
        http_data = self.initialize_data(nginx_topo, "HTTP", "http")
        nginx_topo.component(self.external_id, "nginx_http", http_data)
        for vs_id, virtual_server in self.virtual_servers.items():
            virtual_server.create_virtual_server(self, nginx_topo)


class VirtualServer(Topo):
    def __init__(self, id, external_id, filename, line):
        Topo.__init__(self, id, external_id, filename, line)
        self.listen = None
        self.status_zone = None
        self.locations = {}

    # Create virtual server in stackstate
    def create_virtual_server(self, http, nginx_topo):
        server_data = self.initialize_data(nginx_topo, "Virtual Server", self.listen)
        if self.status_zone:
            server_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.component(self.external_id, "nginx_virtual_server", server_data)
        nginx_topo.relation(http.external_id, self.external_id, "has", {})
        for l_id, location in self.locations.items():
            location.create_location(self, nginx_topo)


class Location(Topo):
    def __init__(self, id, external_id, filename, line, location_name):
        Topo.__init__(self, id, external_id, filename, line)
        self.location_name = location_name
        self.status_zone = None
        # The upstream servers
        self.proxy_pass = None  # String representing the proxy value
        self.upstream = None  # Actual proxy pass upstream object

    # Create location in stackstate
    def create_location(self, virtual_server, nginx_topo):
        location_data = self.initialize_data(nginx_topo,  "Location", self.location_name)
        if self.status_zone:
            location_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.log.debug("Location id: {} - data: {}".format(self.external_id, location_data))
        nginx_topo.component(self.external_id, "nginx_location", location_data)
        nginx_topo.relation(virtual_server.external_id, self.external_id, "has", {})
        if self.upstream:
            self.upstream.create_upstream(self, nginx_topo)


class Upstream(Topo):
    def __init__(self, id, external_id, filename, line):
        Topo.__init__(self, id, external_id, filename, line)
        self.upstream_name = None
        self.status_zone = None
        # The upstream servers
        self.servers = {}

    # Create upstream in stackstate
    def create_upstream(self, location, nginx_topo):
        upstream_data = self.initialize_data(nginx_topo, "Upstream", self.upstream_name)
        if self.status_zone:
            upstream_data["status_zone"] = "{}".format(self.status_zone)
        nginx_topo.component(self.external_id, "nginx_upstream", upstream_data)
        nginx_topo.relation(location.external_id, self.external_id, "has", {})
        for s_id, server in self.servers.items():
            server.create_server(self, nginx_topo)


# Corresponds with an upstream server
class Server(Topo):
    def __init__(self, id, external_id, filename, line, server_name):
        Topo.__init__(self, id, external_id, filename, line)
        self.server_name = server_name

    # Create upstream server in stackstate
    def create_server(self, upstream, nginx_topo):
        upstream_server_data = self.initialize_data(nginx_topo, "Upstream Server", self.server_name)
        upstream_server_data["upstream"] = "{}".format(upstream.upstream_name)
        nginx_topo.component(self.external_id, "nginx_upstream_server", upstream_server_data)
        nginx_topo.relation(upstream.external_id, self.external_id, "has", {})


class NginxTopo(AgentCheck):
    INSTANCE_TYPE = "nginx"
    SERVICE_CHECK_NAME = "NginxTopo"

    def __init__(self, name, init_config, instances=None):
        AgentCheck.__init__(self, name, init_config, instances)
        self.payload = None
        self.baseurl = None
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
        name, location, baseurl = self._get_config(instance)
        self.name = name
        self.baseurl = baseurl
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
        return (instance["name"], instance["location"], instance["scm"] if 'scm' in instance else None)

    def _parse_topology(self):
        if self.payload['status'] != "ok" or len(self.payload["errors"]) > 0:
            raise ConfigError("Incorrect payload: {status} - {errors}"
                              .format(status=self.payload['status'],
                                      errors="|".join(error['error'] for error in self.payload['errors'])))
        if len(self.payload['config']) > 0:
            self.filename_base = os.path.dirname(self.payload['config'][0]['file']) + "/"
            self._process_config(self.payload['config'][0])

    def _process_config(self, config, parent=None):
        self.log.debug("Processing config: {}".format(config['file']))
        if config['status'] != "ok" or len(config['errors']) > 0:
            raise "incorrect payload config: {file}".format(file=config['file'])
        for parsed in config['parsed']:
            self._process_parsed(parsed=parsed, parent=parent, filename=config['file'].replace(self.filename_base, ''))

    def _process_parsed(self, parsed, parent, filename):
        id = str(uuid.uuid4())
        self.log.debug("Processing id: {}".format(id))
        if parsed['directive'] == 'upstream':
            # An upstream directive should be parsed later, when the proxy_pass / location directives have been parsed.
            self.upstreams[parsed['args'][0]] = {"filename": filename, "parsed": parsed}
            return
        if parsed['directive'] == 'include':
            for include in parsed['includes']:
                self._process_config(self.payload['config'][include], parent=parent)
        new_parent = self._directive_to_method(parsed, id, parent, filename)

        self.log.debug("Done processing id: {}".format(id))
        if 'block' in parsed:
            for block in parsed['block']:
                if block['directive'] == "include":
                    for include in block['includes']:
                        self._process_config(self.payload['config'][include], parent=new_parent)
                else:
                    self._process_parsed(parsed=block, parent=new_parent, filename=filename)

    def _directive_to_method(self, parsed, id, parent, filename):
        """Dispatch method"""
        method_name = '_directive_' + str(parsed['directive'])
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, None)
        # Call the method as we return it
        return method(parsed, id, parent, filename) if method else None

    def _directive_http(self, parsed, id, parent, filename):
        external_id = "urn:nginx:{}:http".format(self.name)
        self.http = Http(id=id, external_id=external_id, filename=filename, line=parsed['line'])
        return self.http

    def _directive_server(self, parsed, id, parent, filename):
        self.log.debug("Processing directive server for {}".format(id))
        external_id = "urn:nginx:{}:server:{}".format(self.name, "unknown")
        parent.virtual_servers[id] = VirtualServer(id=id, external_id=external_id, filename=filename,
                                                   line=parsed['line'])
        return parent.virtual_servers[id]

    def _directive_listen(self, parsed, id, parent, filename):
        parent.listen = ":".join(parsed['args'])
        external_id = "urn:nginx:{}:server:{}".format(self.name, parent.listen)
        parent.external_id = external_id

    def _directive_status_zone(self, parsed, id, parent, filename):
        parent.status_zone = parsed['args'][0]

    def _directive_location(self, parsed, id, parent, filename):
        location_name = ":".join(parsed['args'])
        external_id = "urn:nginx:{}:server:{}:location:{}".format(self.name, parent.listen,
                                                                  location_name)
        parent.locations[id] = Location(id=id, external_id=external_id, filename=filename, line=parsed['line'],
                                        location_name=location_name)
        return parent.locations[id]

    def _directive_proxy_pass(self, parsed, id, parent, filename):
        parent.proxy_pass = parsed['args'][0]

    def _parse_upstreams(self):
        for vkey, vserver in self.http.virtual_servers.items():
            for lkey, location in vserver.locations.items():
                if location.proxy_pass:
                    self._process_upstream(location)

    def _process_upstream(self, location):
        self.log.debug("Processing upstream {}".format(location.proxy_pass))
        upstream_name = urlparse(location.proxy_pass).netloc
        parsed = self.upstreams[upstream_name]["parsed"]
        filename = self.upstreams[upstream_name]["filename"]
        upstream_id = str(uuid.uuid4())
        upstream_ext_id = "urn:nginx:{}:upstream:{}".format(self.name, upstream_name)
        location.upstream = Upstream(upstream_id, upstream_ext_id, filename=filename, line=parsed['line'])
        location.upstream.upstream_name = upstream_name
        for block in parsed['block']:
            if block['directive'] == 'server':
                server_id = str(uuid.uuid4())
                server_name = ":".join(block['args'])
                server_external_id = "urn:nginx:{}:upstream:{}:server:{}".format(self.name,
                                                                                 upstream_name,
                                                                                 server_name)
                location.upstream.servers[server_id] = Server(server_id, server_external_id, filename=filename,
                                                              line=block['line'], server_name=server_name)
            if block['directive'] == 'zone':
                location.upstream.status_zone = block['args'][0]

    def _create_topology(self):
        if self.http:
            self.http.create_http(self)
