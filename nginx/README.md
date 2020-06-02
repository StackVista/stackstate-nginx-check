# Agent Check: Nginx

## Overview

This check monitors [Nginx][1] through the StackState Agent.

## Setup

### Installation

The Nginx check is included in the [StackState Agent][2] package, so you do not
need to install anything else on your server.

### Configuration

1. Edit the `nginx.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your nginx performance data.
   See the [sample nginx.d/conf.yaml][2] for all available configuration options.

2. Restart the Agent

## Data Collected

### Metrics

Nginx does not include any metrics.

### Service Checks

Nginx does not include any service checks.

### Events

Nginx does not include any events.

### Topology

Nginx does not include any topology.

[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://github.com/StackVista/stackstate-agent-integrations/blob/master/nginx/stackstate_checks/nginx/data/conf.yaml.example
