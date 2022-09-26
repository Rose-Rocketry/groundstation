FROM alpine:3 AS base
# libgcc libstdc++
RUN apk add --no-cache openssl libstdc++

FROM base AS build
WORKDIR /app
RUN apk add --no-cache g++ make cmake git openssl-dev
RUN git clone https://github.com/eclipse/paho.mqtt-sn.embedded-c . && git checkout 59797127e7f3d024de576555cd4232c68e874ac6
RUN mkdir build && cd build && cmake -DSENSORNET=xbee .. && make -j

FROM base AS deploy
COPY --from=build /app/MQTTSNGateway/bin/MQTT-SNGateway /usr/bin/
COPY --from=build /app/build/MQTTSNPacket/src/libMQTTSNPacket.so /usr/lib/
COPY clients.conf gateway.conf /app/

CMD [ "MQTT-SNGateway", "-f", "/app/gateway.conf" ]
