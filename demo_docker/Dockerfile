FROM ubuntu:22.04

ARG VERSION

RUN apt update && apt install -y wget unzip
RUN wget https://github.com/acompany-develop/Gramine-EIM-Synth-DEMO/releases/download/${VERSION}/Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
RUN unzip Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
RUN mkdir -p /usr/lib/x86_64-linux-gnu/ && cp -r usr-lib-x86_64-linux-gnu/* /usr/lib/x86_64-linux-gnu/
RUN mkdir -p /usr/local/lib/x86_64-linux-gnu/ && cp -r usr-local-lib-x86_64-linux-gnu/* /usr/local/lib/x86_64-linux-gnu/
