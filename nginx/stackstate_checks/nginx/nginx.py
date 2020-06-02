# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.base import AgentCheck, ConfigurationError, TopologyInstance
import crossplane


class NginxCheck(AgentCheck):
    INSTANCE_TYPE = "nginx"
    SERVICE_CHECK_NAME = "Nginx"

    def get_instance_key(self, instance):
        if "name" not in instance:
            raise ConfigurationError("Missing name in topology instance configuration.")
        if "location" not in instance:
            raise ConfigurationError("Missing location in topology instance configuration.")

        location = instance["location"]
        return TopologyInstance(self.INSTANCE_TYPE, location)

    def check(self, instance):
        name, location = self._get_config(instance)
        self.start_snapshot()
        try:
            self.log.info("Processing file: {file}".format(file=location))
            payload = crossplane.parse(location)
            self._parse_topology(payload)
        except Exception as err:
            msg = "Nginx check failed: {}".format(str(err))
            self.log.error(msg)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=msg, tags=[])
        finally:
            self.stop_snapshot()

    def _get_config(self, instance):
        return (instance["name"], instance["location"])

    def _parse_topology(self, payload):
        if payload['status'] != "ok" or len(payload["errors"]) > 0:
            raise "incorrect payload"
        for config in payload['config']:
            self._process_config(config)

    def _process_config(self, config):
        if config['status'] != "ok" or len(config['errors']) > 0:
            raise "incorrect payload config: {file}".format(file=config['file'])
        for parsed in config['parsed']:
            self._process_parsed(config['file'], parsed)

    def _process_parsed(self, filename, parsed):
        if parsed['directive'] == 'http':
            external_id = "urn:nginx:http:{}".format(filename)
            self.component(external_id, 'http', {})


