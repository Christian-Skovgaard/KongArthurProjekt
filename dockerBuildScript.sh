#!/bin/bash

NETWORK_NAME="arthur_network"

RESEVATION_IMAGE="resavation_image"
RESEVATION_NAME="resevation_service"
RESEVATION_PORT=5001

ROOM_IMAGE="room_image"
ROOM_NAME="room_scheduling_service"
ROOM_PORT=5002


echo "Building Docker images"
docker build -t $RESEVATION_IMAGE ./resevationService
docker build -t $ROOM_IMAGE ./roomSchedulingService

echo "Creating Docker network: $NETWORK_NAME"
docker network create $NETWORK_NAME

echo "Running containers"
docker run -d --name $RESEVATION_NAME --network $NETWORK_NAME -p $RESEVATION_PORT:5000 $RESEVATION_IMAGE
docker run -d --name $ROOM_NAME --network $NETWORK_NAME -p $ROOM_PORT:5000 $ROOM_IMAGE

echo "Containers in $NETWORK_NAME:"
docker ps --filter "network=$NETWORK_NAME"


