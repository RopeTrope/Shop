docker network create shop-network
docker network create shop-stats

docker build -f .\shop\owner.dockerfile -t owner-app:latest .
docker build -f .\shop\customer.dockerfile -t customer-app:latest .
docker build -f .\shop\courier.dockerfile -t courier-app:latest .

cd .\spark\

docker build -f .\spark.dockerfile -t sparkapp:latest .

docker compose -f .\spark.yaml up -d

Start-Sleep -Seconds 15

cd ..

docker compose up -d


do{
    $input = Read-Host "Press 'x' to stop services..."
} while ( $input.ToLower() -ne 'x' )


docker compose down

docker compose -f .\spark\spark.yaml down