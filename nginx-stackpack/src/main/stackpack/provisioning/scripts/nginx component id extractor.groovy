element = struct.asReadonlyMap()

externalId = element["externalId"]
type = element["typeName"].toLowerCase()
data = element["data"]

identifiers = new HashSet()
identifiers.add(externalId)
if(data.containsKey("identifiers") && data["identifiers"] instanceof List<String>) {
    data["identifiers"].each{ id ->
        identifiers.add(id)
    }
}

if(data.containsKey("instanceTags")) {
    instanceTags = []
    data["instanceTags"].each{ id ->
        instanceTags.add(id)
    }
}

return Sts.createId(externalId, identifiers, type)
