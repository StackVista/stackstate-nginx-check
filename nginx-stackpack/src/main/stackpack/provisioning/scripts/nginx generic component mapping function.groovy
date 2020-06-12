metric_streams = []
metric_zone = "tags.server_zone"

switch (element.type.name) {
    case 'nginx_virtual_server':
        if(element.data.containsKey("status_zone")){
            metric_zone = "tags.server_zone"
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
    default:
        result = 'Default'
        break
}

element.data.put('metric_zone', metric_zone)
element.data.put('nginx_metric_streams', metric_streams)

element
