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

# Step 2: Create a Docker network
echo "Creating Docker network: $NETWORK_NAME"
docker network create $NETWORK_NAME

# Step 3: Run containers
echo "Running $RESEVATION_NAME container..."
docker run -d --name $RESEVATION_NAME --network $NETWORK_NAME -p $RESEVATION_PORT:5000 $RESEVATION_IMAGE

echo "Running $ROOM_NAME container..."
docker run -d --name $ROOM_NAME --network $NETWORK_NAME $ROOM_IMAGE

# Step 4: Verify containers are running
echo "Containers in network $NETWORK_NAME:"
docker ps --filter "network=$NETWORK_NAME"

# Step 5: Test connectivity
echo "Testing connectivity from $RESEVATION_NAME to $ROOM_NAME..."
docker exec -it $RESEVATION_NAME curl -s http://$ROOM_NAME:5000/test

# Step 6: Print instructions
echo ""
echo "Flask App 1 is running on http://localhost:$PORT"
echo "Flask App 2 is accessible from App 1 using the hostname: $ROOM_NAME"
echo "Try calling http://localhost:$PORT/call_app2 to see the communication in action."
