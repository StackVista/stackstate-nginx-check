def nginxSync = component.synced.find { s ->
    Graph.query({
        it
        .V(s.sync)[0]
        .property('name').value().contains("nginx")
    })
}

UI.redirectToURL(nginxSync.extTopologyElement.data.scm)