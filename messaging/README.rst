Fire up

1)
../bin/pserve messaging.ini --reload

2)
make get request
curl -X GET localhost:6543/corp

make post request
curl -X POST localhost:6543/corp -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job"}}'
