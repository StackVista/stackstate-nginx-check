# (C) Datadog, Inc. 2018-present
# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)


# Map metrics from vhost_traffic_status to metrics from NGINX Plus
VTS_METRIC_MAP = {
    'nginx.loadMsec': 'nginx.load_timestamp',
    'nginx.nowMsec': 'nginx.timestamp',
    'nginx.connections.accepted': 'nginx.connections.accepted',
    'nginx.connections.active': 'nginx.connections.active',
    'nginx.connections.reading': 'nginx.net.reading',
    'nginx.connections.writing': 'nginx.net.writing',
    'nginx.connections.waiting': 'nginx.net.waiting',
    'nginx.connections.requests': 'nginx.requests.total',
    'nginx.server_zone.requestCounter': 'nginx.server_zone.requests',
    'nginx.server_zone.responses.1xx': 'nginx.server_zone.responses.1xx',
    'nginx.server_zone.responses.2xx': 'nginx.server_zone.responses.2xx',
    'nginx.server_zone.responses.3xx': 'nginx.server_zone.responses.3xx',
    'nginx.server_zone.responses.4xx': 'nginx.server_zone.responses.4xx',
    'nginx.server_zone.responses.5xx': 'nginx.server_zone.responses.5xx',
    'nginx.server_zone.inBytes': 'nginx.server_zone.received',
    'nginx.server_zone.outBytes': 'nginx.server_zone.sent',
    'nginx.upstream.requestCounter': 'nginx.upstream.peers.requests',
    'nginx.upstream.inBytes': 'nginx.upstream.peers.received',
    'nginx.upstream.outBytes': 'nginx.upstream.peers.sent',
    'nginx.upstream.responses.1xx': 'nginx.upstream.peers.responses.1xx',
    'nginx.upstream.responses.2xx': 'nginx.upstream.peers.responses.2xx',
    'nginx.upstream.responses.3xx': 'nginx.upstream.peers.responses.3xx',
    'nginx.upstream.responses.4xx': 'nginx.upstream.peers.responses.4xx',
    'nginx.upstream.responses.5xx': 'nginx.upstream.peers.responses.5xx',
    'nginx.upstream.weight': 'nginx.upstream.peers.weight',
    'nginx.upstream.backup': 'nginx.upstream.peers.backup',
    'nginx.upstream.down': 'nginx.upstream.peers.health_checks.last_passed',
}

METRICS_SEND_AS_COUNT = [
    'nginx.upstream.peers.responses.1xx',
    'nginx.upstream.peers.responses.2xx',
    'nginx.upstream.peers.responses.3xx',
    'nginx.upstream.peers.responses.4xx',
    'nginx.upstream.peers.responses.5xx',
    'nginx.upstream.peers.received',
    'nginx.upstream.peers.sent',
    'nginx.server_zone.responses.1xx',
    'nginx.server_zone.responses.2xx',
    'nginx.server_zone.responses.3xx',
    'nginx.server_zone.responses.4xx',
    'nginx.server_zone.responses.5xx',
    'nginx.server_zone.received',
    'nginx.server_zone.sent',
    'nginx.cache.bypass.bytes',
    'nginx.cache.bypass.bytes_written',
    'nginx.cache.bypass.responses',
    'nginx.cache.bypass.responses_written',
    'nginx.cache.expired.bytes',
    'nginx.cache.expired.bytes_written',
    'nginx.cache.expired.responses',
    'nginx.cache.expired.responses_written',
    'nginx.cache.hit.bytes',
    'nginx.cache.hit.responses',
    'nginx.cache.miss.bytes',
    'nginx.cache.miss.bytes_written',
    'nginx.cache.miss.responses',
    'nginx.cache.miss.responses_written',
    'nginx.cache.revalidated.bytes',
    'nginx.cache.revalidated.response',
    'nginx.cache.stale.bytes',
    'nginx.cache.stale.responses',
    'nginx.cache.updating.bytes',
    'nginx.cache.updating.responses',
    'nginx.connections.accepted',
    'nginx.connections.dropped',
    'nginx.generation',
    'nginx.processes.respawned',
    'nginx.requests.total',
    'nginx.server_zone.discarded',
    'nginx.server_zone.requests',
    'nginx.server_zone.responses.total',
    'nginx.slab.slots.fails',
    'nginx.slab.slots.reqs',
    'nginx.ssl.handshakes',
    'nginx.ssl.handshakes_failed',
    'nginx.ssl.session_reuses',
    'nginx.stream.server_zone.connections',
    'nginx.stream.server_zone.discarded',
    'nginx.stream.server_zone.received',
    'nginx.stream.server_zone.sent',
    'nginx.stream.server_zone.sessions.2xx',
    'nginx.stream.server_zone.sessions.4xx',
    'nginx.stream.server_zone.sessions.5xx',
    'nginx.stream.server_zone.sessions.total',
    'nginx.stream.upstream.peers.connections',
    'nginx.stream.upstream.peers.fails',
    'nginx.stream.upstream.peers.health_checks.checks',
    'nginx.stream.upstream.peers.health_checks.fails',
    'nginx.stream.upstream.peers.health_checks.unhealthy',
    'nginx.stream.upstream.peers.received',
    'nginx.stream.upstream.peers.sent',
    'nginx.stream.upstream.peers.unavail',
    'nginx.upstream.peers.fails',
    'nginx.upstream.peers.health_checks.checks',
    'nginx.upstream.peers.health_checks.fails',
    'nginx.upstream.peers.health_checks.unhealthy',
    'nginx.upstream.peers.requests',
    'nginx.upstream.peers.responses.total',
    'nginx.upstream.peers.unavail',
]
