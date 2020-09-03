FROM openfaas/classic-watchdog:0.18.1 as watchdog

FROM debian:buster-slim
LABEL maintainer "StackState <info@stackstate.com>"

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
RUN apt-get update && apt-get install -y \
    curl \
 && rm -rf /var/lib/apt/lists/*

RUN curl -o- https://stackstate-agent-2.s3.amazonaws.com/install.sh | STS_API_KEY="STS_API_KEY_PLACEHOLDER" STS_URL="STS_URL_PLACEHOLDER" STS_INSTALL_ONLY="true" bash

USER stackstate-agent

RUN mkdir -p /etc/stackstate-agent/checks.d/nginxmetrics \
    && mkdir -p /etc/stackstate-agent/conf.d/nginxmetrics.d

COPY --chown=stackstate-agent:stackstate-agent tmp/conf.yaml.docker.example /etc/stackstate-agent/conf.d/nginxmetrics.d/conf.yaml
COPY --chown=stackstate-agent:stackstate-agent tmp/*.py /etc/stackstate-agent/checks.d/nginxmetrics/

COPY resources/run.sh /usr/bin/run.sh
ENV fprocess="xargs /usr/bin/run.sh"
# Set to true to see request in function logs
ENV write_debug="false"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]