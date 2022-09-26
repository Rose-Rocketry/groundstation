FROM alpine:3 AS base
RUN apk add --no-cache openssl libstdc++

FROM base AS build
WORKDIR /app
RUN apk add --no-cache g++ ninja cmake git openssl-dev
RUN git clone https://github.com/eclipse/paho.mqtt-sn.embedded-c . && git checkout 59797127e7f3d024de576555cd4232c68e874ac6

ARG SENSORNET=xbee
WORKDIR /app/build
RUN cmake -GNinja -DSENSORNET=${SENSORNET} ..
RUN ninja MQTT-SNGateway

FROM base AS deploy
COPY --from=build /app/MQTTSNGateway/bin/MQTT-SNGateway /usr/bin/
COPY --from=build /app/build/MQTTSNPacket/src/libMQTTSNPacket.so /usr/lib/
COPY clients.conf gateway.conf /app/

CMD [ "MQTT-SNGateway", "-f", "/app/gateway.conf" ]
