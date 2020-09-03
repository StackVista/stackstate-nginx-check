#!/usr/bin/env bash

# Replace env vars in /etc/stackstate-agent/stackstate.yaml
sed -i "s/STS_API_KEY_PLACEHOLDER/$sts_api_key/g" /etc/stackstate-agent/stackstate.yaml
sed -i "s,STS_URL_PLACEHOLDER,$sts_receiver_api,g" /etc/stackstate-agent/stackstate.yaml

# Replace env vars in /etc/stackstate-agent/conf.d/nginxtopo.d/conf.yaml
sed -i "s,STS_NGINXTOPO_LOCATION,$sts_nginxtopo_location,g" /etc/stackstate-agent/conf.d/nginxtopo.d/conf.yaml
sed -i "s/STS_NGINXTOPO_NAME/$sts_nginxtopo_name/g" /etc/stackstate-agent/conf.d/nginxtopo.d/conf.yaml
sed -i "s,STS_NGINXTOPO_SCM,$sts_nginxtopo_scm,g" /etc/stackstate-agent/conf.d/nginxtopo.d/conf.yaml

# Download nginx config and extract at location
topo_config_dir=/etc/stackstate-agent/topo
mkdir -p $topo_config_dir
http -d GET $sts_nginxtopo_download -o $topo_config_dir/download.zip
unzip -q -o $topo_config_dir/download.zip -d $(dirname $sts_nginxtopo_location)

stackstate-agent run &
sleep 10
stackstate-agent stop
