metric_streams = []

switch (element.type.name) {
    case 'nginx_virtual_server':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.server_zone"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "The number of client requests that are currently being processed.", value: "nginx.server_zone.processing", id: "-1001", aggregation: "MAX"],
                [ name: "The total number of client requests received from clients.", value: "nginx.server_zone.requests", id: "-1002", aggregation: "MAX"],
                [ name: "The number of responses with 1xx status codes.", value: "nginx.server_zone.responses.1xx", id: "-1003", aggregation: "MAX"],
                [ name: "The number of responses with 2xx status codes.", value: "nginx.server_zone.responses.2xx", id: "-1004", aggregation: "MAX"],
                [ name: "The number of responses with 3xx status codes.", value: "nginx.server_zone.responses.3xx", id: "-1005", aggregation: "MAX"],
                [ name: "The number of responses with 4xx status codes.", value: "nginx.server_zone.responses.4xx", id: "-1006", aggregation: "MAX"],
                [ name: "The number of responses with 5xx status codes.", value: "nginx.server_zone.responses.5xx", id: "-1007", aggregation: "MAX"],
                [ name: "The total number of responses sent to clients.", value: "nginx.server_zone.responses.total", id: "-1008", aggregation: "MAX"],
                [ name: "The total number of bytes sent to clients.", value: "nginx.server_zone.sent", id: "-1009", aggregation: "MAX"],
                [ name: "The total number of bytes received from clients.", value: "nginx.server_zone.received", id: "-1010", aggregation: "MAX"],
            ])
        }
        break
    case 'nginx_location':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.location_zone"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "The total number of client requests received from clients.", value: "nginx.location_zone.requests", id: "-2001", aggregation: "MAX"],
                [ name: "The number of responses with 1xx status codes.", value: "nginx.location_zone.responses.1xx", id: "-2002", aggregation: "MAX"],
                [ name: "The number of responses with 2xx status codes.", value: "nginx.location_zone.responses.2xx", id: "-2003", aggregation: "MAX"],
                [ name: "The number of responses with 3xx status codes.", value: "nginx.location_zone.responses.3xx", id: "-2004", aggregation: "MAX"],
                [ name: "The number of responses with 4xx status codes.", value: "nginx.location_zone.responses.4xx", id: "-2005", aggregation: "MAX"],
                [ name: "The number of responses with 5xx status codes.", value: "nginx.location_zone.responses.5xx", id: "-2006", aggregation: "MAX"],
                [ name: "The total number of responses sent to clients.", value: "nginx.location_zone.responses.total", id: "-2007", aggregation: "MAX"],
                [ name: "The total number of bytes sent to clients.", value: "nginx.location_zone.sent", id: "-2008", aggregation: "MAX"],
                [ name: "The total number of bytes received from clients.", value: "nginx.location_zone.received", id: "-2009", aggregation: "MAX"],
            ])
        }
        break
    case 'nginx_upstream':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.slab"
            element.data.put('metric_zone', metric_zone)
            metric_streams = metric_streams.plus([
                [ name: "The current number of free memory pages.", value: "nginx.slab.pages.free", id: "-3001", aggregation: "MAX"],
                [ name: "The current number of used memory pages.", value: "nginx.slab.pages.used", id: "-3002", aggregation: "MAX"],
            ])
            element.data.put('checks', true)
        }
        break
    case 'nginx_upstream_server':
        metric_streams = metric_streams.plus([
                [ name: "Total time the server was in the “unavail”, “checking”, and “unhealthy” states.", value: "nginx.upstream.peers.downtime", id: "-4001", aggregation: "MAX"],
                [ name: "The weight of the server", value: "nginx.upstream.peers.weight", id: "-4002", aggregation: "MAX"],
                [ name: "The total number of client requests forwarded to this server.", value: "nginx.upstream.peers.requests", id: "-4003", aggregation: "MAX"],
                [ name: "The number of responses with “1xx” status codes.", value: "nginx.upstream.peers.responses.1xx", id: "-4004", aggregation: "MAX"],
                [ name: "The number of responses with “2xx” status codes.", value: "nginx.upstream.peers.responses.2xx", id: "-4005", aggregation: "MAX"],
                [ name: "The number of responses with “3xx” status codes.", value: "nginx.upstream.peers.responses.3xx", id: "-4006", aggregation: "MAX"],
                [ name: "The number of responses with “4xx” status codes.", value: "nginx.upstream.peers.responses.4xx", id: "-4007", aggregation: "MAX"],
                [ name: "The number of responses with “5xx” status codes.", value: "nginx.upstream.peers.responses.5xx", id: "-4008", aggregation: "MAX"],
                [ name: "The current number of active connections.", value: "nginx.upstream.peers.active", id: "-4009", aggregation: "MAX"],
                [ name: "The max_conns limit for the server.", value: "nginx.upstream.peers.max_conns", id: "-4010", aggregation: "MAX"],
                [ name: "The total number of bytes sent to this server.", value: "nginx.upstream.peers.sent", id: "-4011", aggregation: "MAX"],
                [ name: "The total number of bytes received from this server.", value: "nginx.upstream.peers.received", id: "-4012", aggregation: "MAX"],
                [ name: "The total number of unsuccessful attempts to communicate with the server.", value: "nginx.upstream.peers.fails", id: "-4013", aggregation: "MAX"],
                [ name: "How many times the server became unavailable for client requests (state “unavail”) due to the number of unsuccessful attempts reaching the max_fails threshold.", value: "nginx.upstream.peers.unavail", id: "-4014", aggregation: "MAX"],
                [ name: "The total number of health check requests made.", value: "nginx.upstream.peers.health_checks.checks", id: "-4015", aggregation: "MAX"],
                [ name: "The number of failed health checks.", value: "nginx.upstream.peers.health_checks.fails", id: "-4016", aggregation: "MAX"],
                [ name: "How many times the server became unhealthy (state “unhealthy”).", value: "nginx.upstream.peers.health_checks.unhealthy", id: "-4017", aggregation: "MAX"],
                [ name: "Boolean indicating if the last health check request was successful and passed tests.", value: "nginx.upstream.peers.health_checks.last_passed", id: "-4018", aggregation: "MAX"],
                [ name: "The average time to get the response header from the server.", value: "nginx.upstream.peers.header_time", id: "-4019", aggregation: "MAX"],
                [ name: "The average time to get the full response from the server.", value: "nginx.upstream.peers.response_time", id: "-4020", aggregation: "MAX"],
        ])
        break
    default:
        result = 'Default'
        break
}

element.data.put('nginx_metric_streams', metric_streams)

element
