#### Prerequisites

The following prerequisites need to be met:

* StackState Agent V2 must be installed on a single machine which can connect to StackState. (See the [StackState Agent V2 StackPack](/#/stackpacks/stackstate-agent-v2/) for more details)


#### Enabling Nginx check
To enable the Nginx topology check which collects the data from Nginx instance:

Edit the `conf.yaml` file in your agent `/etc/stackstate-agent/conf.d/nginxtopo.d` directory, replacing `<name>` with your nginx name and `<location>` with location to where the `nginx.conf` can be found. `<scm>` points to a base SCM url where the nginx config can be found (Optional)

```
# Section used for Nginx Topo check config
init_config: {}
instances:
  - location: /etc/nginx/nginx.conf
    name: stsdemo
    scm: https://github.com/jdewinne/stackstate-nginx-check/blob/main/nginx/tests/data/complex
```

To enable the Nginx metrics check which collects the data from Nginx instance:

Edit the `conf.yaml` file in your agent `/etc/stackstate-agent/conf.d/nginxmetrics.d` directory, replacing `<nginx_status_url>` with your nginx status api url endpoint, `<use_plus_api>` to `true` if Nginx+ is used and `<plus_api_version>` to the corresponding Nginx+ api version.

```
init_config:
## Every instance is scheduled independent of the others.
#
instances:
  - nginx_status_url: http://localhost:81/nginx_status/
    use_plus_api: true
    plus_api_version: 6
    tags:
      - nginx_name:stsdemo

```

To publish the configuration changes, restart the StackState Agent(s).

Once the Agent is restarted, wait for the Agent to collect the data and send it to StackState.
