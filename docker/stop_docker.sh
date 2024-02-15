PROJECT_NAME=Shekhar-IQ

docker network rm ${PROJECT_NAME}-network


echo "Starting Postgres related containers"
docker-compose -f ./docker/postgres/docker-compose.yml down 
echo "  "

echo "Starting Mage container"
docker-compose -f ./docker/mage/docker-compose.yml down 
echo "  "

echo "Starting Metabase container"
docker-compose -f ./docker/metabase/docker-compose.yml down 
echo "  "

echo "Starting Kafka related containers"
docker-compose -f ./docker/kafka/docker-compose.yml down 
echo "  "

echo "Starting Spark related containers"

docker-compose -f ./docker/spark/sparkdocker/docker-compose.yml down
echo "  "

echo "Started all containers you can check their ps here:"
