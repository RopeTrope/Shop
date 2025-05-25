docker network create shop-network
docker network create shop-stats

docker build -f .\shop\owner.dockerfile -t owner-app:latest .
docker build -f .\shop\customer.dockerfile -t customer-app:latest .
docker build -f .\shop\courier.dockerfile -t courier-app:latest .

cd .\spark\

docker build -f .\spark.dockerfile -t sparkapp:latest .

docker compose -f .\spark.yaml up -d

cd ..

docker compose up 