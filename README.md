# technopark_sa_proxy

Сгенерировать сертификаты:
```
./gen_ca.sh
```

Запуск прокси:
```
make proxy
```

Запуск веб-интерфейса (можно посмотреть в браузере):
```
make web
```

Запросы:
```
127.0.0.0:5000/requests – список запросов
127.0.0.0:5000/requests/id – вывод 1 запроса
127.0.0.0:5000/repeat/id – повторная отправка запроса
127.0.0.0:5000/scan/id – сканирование запроса
```
