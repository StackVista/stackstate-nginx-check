# (C) StackState 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from stackstate_checks.nginx import NginxCheck
from stackstate_checks.base.stubs import topology


def test_basic_http(aggregator, http_instance):
    check = NginxCheck('nginx', {}, instances=[http_instance])
    check.check(http_instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    relations = snapshot.get("relations")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': http_instance['location']}
    assert len(components) == 1
    assert len(relations) == 0
    assert instance_key == expected_instance_key


def test_basic_events(aggregator, events_instance):
    topology.reset()
    check = NginxCheck('nginx', {}, instances=[events_instance])
    check.check(events_instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    relations = snapshot.get("relations")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': events_instance['location']}
    # since we do not support events, no components are created at the moment.
    assert len(components) == 0
    assert len(relations) == 0
    assert instance_key == expected_instance_key


def test_simple(aggregator, simple_instance):
    topology.reset()
    check = NginxCheck('nginx', {}, instances=[simple_instance])
    check.check(simple_instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    relations = snapshot.get("relations")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': simple_instance['location']}
    assert len(components) == 3
    assert len(relations) == 2
    assert instance_key == expected_instance_key


def test_messy(aggregator, messy_instance):
    topology.reset()
    check = NginxCheck('nginx', {}, instances=[messy_instance])
    check.check(messy_instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    relations = snapshot.get("relations")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': messy_instance['location']}
    assert len(components) == 11
    assert len(relations) == 10
    assert instance_key == expected_instance_key


def test_include(aggregator, include_instance):
    topology.reset()
    check = NginxCheck('nginx', {}, instances=[include_instance])
    check.check(include_instance)
    snapshot = topology.get_snapshot(check.check_id)
    components = snapshot.get("components")
    relations = snapshot.get("relations")
    instance_key = snapshot.get("instance_key")
    expected_instance_key = {'type': 'nginx', 'url': include_instance['location']}
    assert len(components) == 5
    assert len(relations) == 4
    assert instance_key == expected_instance_key
