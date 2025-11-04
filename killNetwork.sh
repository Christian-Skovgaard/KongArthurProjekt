docker stop resevation_service
docker stop room_scheduling_service

docker rm resevation_service
docker rm room_scheduling_service

docker network rm arthur_network