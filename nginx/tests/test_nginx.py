# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.nginx import NginxCheck
from stackstate_checks.base.stubs import topology


def test_check(aggregator, instance):
    check = NginxCheck('nginx', {}, {}, instances=[instance])
    check.check(instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': instance['location']}
    # since the default instance is not configured, no components are created at the moment.
    assert len(components) == 1
    assert instance_key == expected_instance_key
