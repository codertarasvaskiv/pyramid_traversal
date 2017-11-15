Fire up

1)
../bin/pserve messaging.ini --reload

2)
make get request
curl -X GET localhost:6543/corp

make post request dont work cuz we need authorization
curl -X POST localhost:6543/corp -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job"}}'
here work
curl -X POST localhost:6543/corp -H "Authorization: taras" -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job12"}}'

