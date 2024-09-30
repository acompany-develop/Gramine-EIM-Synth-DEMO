FROM ubuntu:22.04

ARG VERSION

RUN apt update && apt install -y wget unzip
# RUN wget https://github.com/acompany-develop/Gramine-EIM-Synth-DEMO/releases/download/${VERSION}/Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
COPY Gramine-EIM-Synth-v${VERSION}-linux-x64.zip .
RUN unzip Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
