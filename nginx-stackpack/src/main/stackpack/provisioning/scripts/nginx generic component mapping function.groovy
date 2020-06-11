metric_streams = []

switch (element.type.name) {
    case 'nginx_virtual_server':
        if(element.data.containsKey("status_zone")){
            metric_streams = metric_streams.plus([
                [ name: "The number of responses with 3xx status codes.", value: "nginx.server_zone.responses.3xx", id: "-1000"]
            ])
        }
        break
    default:
        result = 'Default'
        break
}

element.data.put('nginx_metric_streams', metric_streams)

element
