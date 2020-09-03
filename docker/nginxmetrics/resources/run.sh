#!/usr/bin/env bash

# Replace env vars in /etc/stackstate-agent/stackstate.yaml
sed -i "s/STS_API_KEY_PLACEHOLDER/$sts_api_key/g" /etc/stackstate-agent/stackstate.yaml
sed -i "s,STS_URL_PLACEHOLDER,$sts_receiver_api,g" /etc/stackstate-agent/stackstate.yaml

# Replace env vars in /etc/stackstate-agent/conf.d/nginxmetrics.d/conf.yaml
sed -i "s,STS_NGINXMETRICS_STATUS_URL,$sts_nginxmetrics_status_url,g" /etc/stackstate-agent/conf.d/nginxmetrics.d/conf.yaml
sed -i "s/STS_NGINXMETRICS_TAG_NGINX_NAME/$sts_nginxmetrics_tag_nginx_name/g" /etc/stackstate-agent/conf.d/nginxmetrics.d/conf.yaml

stackstate-agent run &
sleep 20
stackstate-agent stop
