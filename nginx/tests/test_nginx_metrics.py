# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.nginxmetrics import NginxMetrics


def test_demo_nginx_com(aggregator, demo_instance):
    aggregator.reset()
    check = NginxMetrics('nginx', {}, instances=[demo_instance])
    check.check(demo_instance)
    aggregator.assert_metric("nginx.stream.upstream.peers.received")
