Fire up

0) need to fire up couchdb with circus probably

00) also need to install all packages
    how to do that ?
    bin/activate =>  pip install pytz


1)
../bin/pserve messaging.ini --reload

2)
make get request
curl -X GET localhost:6543/corp

make post request dont work cuz we need authorization
curl -X POST localhost:6543/corp -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job"}}'
here work
curl -X POST localhost:6543/corp -H "Authorization: taras" -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job12"}}'

add corporation with departmanrs
curl -X POST localhost:6543/corp -H "Authorization: taras" -H "Content-Type: application/json" -d '{"data": {"name":"taras", "title":"job", "departments": [{"depName": "test", "depTitle": "testTitle"}]}}'
curl -X GET localhost:6543/corp -H "Authorization: oleg" -H "Content-Type: application/json"

get specific tender, need acc_token
curl -X GET localhost:6543/corp/2b748e6c278a4717a15e585fd4427443?acc_token=26714998e9e1408e949d92f5dddbe747 -H "Authorization: oleg" -H "Content-Type: application/json"

make patch request to corporation
curl -X PATCH localhost:6543/corp/472a34ffd7d147cf9e521998c10f56c7?acc_token=c514ba92d9f34888962a3cf5482d8fac -H "Authorization: taras" -H "Content-Type: application/json" -d '{"data": {"name":"name-modified", "title":"job-modified"}}'










auth.py


def unauthenticated_userid  -->  викликає _get_credentials  і якщо є return value  то бере із users і вертає словник
def _get_credentials  -->  бере з реквесту інформацію розкодовує і отримуємо password. В моєму випадку просто імя

def callback  -->  викликає _get_credentials  тоді отримуємо юзера якщо є юзер тоді викликаємо def check. callback має вернути список acl
def check --> перевіряє чи є токен і формує список груп. Тобто ці групи присвоюються юзеру

на вюшку одночасно приходить юзер із своїм списком груп. Які отримали із auth.py.
Тоді контекст при створенні  "викликає" def __acl__ і формується список груп які мають доступ до контексту.
acl це список ключ-значення. Тоді permission бере із acl ті групи які відповідають permission.
Накінець permission-групи порівнюються із тими групами які має юзер. Якщо є співпадіння юзер отримує доступ до вюшки.

в самій вюшці кожен юзер може мати свої окремі права. Через  if self.request.authenticated_role == 'chronograph':
  тобто викликається додатково функція authenticated_role




