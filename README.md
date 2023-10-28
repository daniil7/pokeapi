# pokeapi

Веб сервис для запроса и отображения данных из [pokeapi](https://pokeapi.co/), созданный в образовательных целях.
Стэк технологий: Flask, Tailwind CSS, AlpineJS

## Установка

$ pip3 install -r requirements.txt

### Для разработки

+ установить зависимости npm: $ npm install
+ запустить веб сервер: $ python3 run.py
+ запустить webpack-watch: $ npm run dev

### Билд проекта

$ npm run build

### Переменные среды

Некоторые настройки доступны путём изменения ENV.

$ cp .env.example .env <br />
$ your-favourite-editor .env

## Docker

$ make build
$ docker compose --env-file .env.production up -d
