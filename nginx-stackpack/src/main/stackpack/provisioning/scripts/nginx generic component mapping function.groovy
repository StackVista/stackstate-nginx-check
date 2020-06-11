metric_streams = []

switch (element.type.name) {
    case 'nginx_virtual_server':
        if(element.data.containsKey("status_zone")){
            metric_streams = metric_streams.plus([
                [ name: "The total number of client requests received from clients.", value: "nginx.server_zone.requests", id: "-1001", aggregation: "MAX"],
                [ name: "The number of responses with 1xx status codes.", value: "nginx.server_zone.responses.1xx", id: "-1002", aggregation: "MAX"],
                [ name: "The number of responses with 2xx status codes.", value: "nginx.server_zone.responses.2xx", id: "-1003", aggregation: "MAX"],
                [ name: "The number of responses with 3xx status codes.", value: "nginx.server_zone.responses.3xx", id: "-1004", aggregation: "MAX"],
                [ name: "The number of responses with 4xx status codes.", value: "nginx.server_zone.responses.4xx", id: "-1005", aggregation: "MAX"],
                [ name: "The number of responses with 5xx status codes.", value: "nginx.server_zone.responses.5xx", id: "-1006", aggregation: "MAX"],
                [ name: "The total number of responses sent to clients.", value: "nginx.server_zone.responses.total", id: "-1007", aggregation: "MAX"]
            ])
        }
        break
    default:
        result = 'Default'
        break
}

element.data.put('nginx_metric_streams', metric_streams)

element
