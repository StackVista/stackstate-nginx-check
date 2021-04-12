metric_streams = []

switch (element.type.name) {
    case 'nginx_virtual_server':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.server_zone"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "Request processing", value: "nginx.server_zone.processing", id: "-1001", aggregation: "MAX"],
                [ name: "Request received (total)", value: "nginx.server_zone.requests", id: "-1002", aggregation: "MAX"],
                [ name: "1xx codes (total)", value: "nginx.server_zone.responses.1xx", id: "-1003", aggregation: "MAX"],
                [ name: "2xx codes (total)", value: "nginx.server_zone.responses.2xx", id: "-1004", aggregation: "MAX"],
                [ name: "3xx codes (total)", value: "nginx.server_zone.responses.3xx", id: "-1005", aggregation: "MAX"],
                [ name: "4xx codes (total)", value: "nginx.server_zone.responses.4xx", id: "-1006", aggregation: "MAX"],
                [ name: "5xx codes (total)", value: "nginx.server_zone.responses.5xx", id: "-1007", aggregation: "MAX"],
                [ name: "Responses sent (total)", value: "nginx.server_zone.responses.total", id: "-1008", aggregation: "MAX"],
                [ name: "Bytes sent (total)", value: "nginx.server_zone.sent", id: "-1009", aggregation: "MAX"],
                [ name: "Bytes received (total)", value: "nginx.server_zone.received", id: "-1010", aggregation: "MAX"],
            ])
        }
        break
    case 'nginx_location':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.location_zone"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "Request received (total)", value: "nginx.location_zone.requests", id: "-2001", aggregation: "MAX"],
                [ name: "1xx codes (total)", value: "nginx.location_zone.responses.1xx", id: "-2002", aggregation: "MAX"],
                [ name: "2xx codes (total)", value: "nginx.location_zone.responses.2xx", id: "-2003", aggregation: "MAX"],
                [ name: "3xx codes (total)", value: "nginx.location_zone.responses.3xx", id: "-2004", aggregation: "MAX"],
                [ name: "4xx codes (total)", value: "nginx.location_zone.responses.4xx", id: "-2005", aggregation: "MAX"],
                [ name: "5xx codes (total)", value: "nginx.location_zone.responses.5xx", id: "-2006", aggregation: "MAX"],
                [ name: "Responses sent (total)", value: "nginx.location_zone.responses.total", id: "-2007", aggregation: "MAX"],
                [ name: "Bytes sent (total)", value: "nginx.location_zone.sent", id: "-2008", aggregation: "MAX"],
                [ name: "Bytes received (total)", value: "nginx.location_zone.received", id: "-2009", aggregation: "MAX"],
            ])
        }
        break
    case 'nginx_upstream':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.slab"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "Free memory pages", value: "nginx.slab.pages.free", id: "-3001", aggregation: "MAX"],
                [ name: "Used memory pages", value: "nginx.slab.pages.used", id: "-3002", aggregation: "MAX"],
            ])
            element.data.put('checks', true)
        }
        break
    case 'nginx_upstream_server':
        metric_streams = metric_streams.plus([
                [ name: "Time unhealthy (total)", value: "nginx.upstream.peers.downtime", id: "-4001", aggregation: "MAX"],
                [ name: "Weight", value: "nginx.upstream.peers.weight", id: "-4002", aggregation: "MAX"],
                [ name: "Client requests forwarded (total)", value: "nginx.upstream.peers.requests", id: "-4003", aggregation: "MAX"],
                [ name: "“1xx” codes", value: "nginx.upstream.peers.responses.1xx", id: "-4004", aggregation: "MAX"],
                [ name: "“2xx” codes", value: "nginx.upstream.peers.responses.2xx", id: "-4005", aggregation: "MAX"],
                [ name: "“3xx” codes", value: "nginx.upstream.peers.responses.3xx", id: "-4006", aggregation: "MAX"],
                [ name: "“4xx” codes", value: "nginx.upstream.peers.responses.4xx", id: "-4007", aggregation: "MAX"],
                [ name: "“5xx” codes", value: "nginx.upstream.peers.responses.5xx", id: "-4008", aggregation: "MAX"],
                [ name: "Active connections.", value: "nginx.upstream.peers.active", id: "-4009", aggregation: "MAX"],
                [ name: "The max_conns limit for the server.", value: "nginx.upstream.peers.max_conns", id: "-4010", aggregation: "MAX"],
                [ name: "Bytes sent (total)", value: "nginx.upstream.peers.sent", id: "-4011", aggregation: "MAX"],
                [ name: "Bytes received (total)", value: "nginx.upstream.peers.received", id: "-4012", aggregation: "MAX"],
                [ name: "Unsuccessful attempts (total)", value: "nginx.upstream.peers.fails", id: "-4013", aggregation: "MAX"],
                [ name: "Unavailable time (total)", value: "nginx.upstream.peers.unavail", id: "-4014", aggregation: "MAX"],
                [ name: "Health check requests (total)", value: "nginx.upstream.peers.health_checks.checks", id: "-4015", aggregation: "MAX"],
                [ name: "Failed health checks (total)", value: "nginx.upstream.peers.health_checks.fails", id: "-4016", aggregation: "MAX"],
                [ name: "Unhealthy count (total)", value: "nginx.upstream.peers.health_checks.unhealthy", id: "-4017", aggregation: "MAX"],
                [ name: "Last health check successful", value: "nginx.upstream.peers.health_checks.last_passed", id: "-4018", aggregation: "MAX"],
                [ name: "Get response header latency (average)", value: "nginx.upstream.peers.header_time", id: "-4019", aggregation: "MEAN"],
                [ name: "Response latency (average)", value: "nginx.upstream.peers.response_time", id: "-4020", aggregation: "MEAN"],
        ])
        break
    default:
        result = 'Default'
        break
}

element.data.put('nginx_metric_streams', metric_streams)

element
