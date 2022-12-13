Урок 19. Декораторы и контроль доступа. Домашнее задание

Шаг 1. Клонируйте репозиторий
Шаг 2. Создайте пользователя
Создайте модель и схему пользователя и добавьте к ней CRUD (views с методами GET/POST/PUT).
Шаг 2.1. Добавьте методы генерации хеша пароля пользователя
В слой с бизнес-логикой, хешируем пароли с помощью pbkdf2_hmac.
Шаг 3. Добавьте недостающие методы CBV
У моделей Director и Genre отсутствуют методы POST, PUT, DELETE. Добавьте их.
Добавьте методы в сервис и в DAO.
Шаг 4. Добавьте эндпоинты аутентификации
`POST` /auth/ — возвращает `access_token` и `refresh_token` или `401` Anonymous (кто угодно)
`PUT` /auth/ — возвращает `access_token` и `refresh_token` или `401` Anonymous (кто угодно)

POST /auth — получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД (есть ли
такой пользователь, такой ли у него пароль)и если всё оk — генерит пару access_token и refresh_token и отдает их в виде
JSON.

PUT /auth — получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token и если он не истек и
валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.

Шаг 5. Ограничьте доступ на чтение
Защитите (ограничьте доступ) так, чтобы к некоторым эндпоинтам был ограничен доступ для запросов без токена. Для этого
создайте декоратор auth_required и декорируйте им методы, которые нужно защитить.
`GET` /directors/ + /directors/id Authorized Required

`GET` /movies/ + /movies/id Authorized Required

`GET` /genres/ + /genres/id Authorized Required

Шаг 6. Ограничьте доступ на редактирование
Защитите (ограничьте доступ) так, чтобы к некоторым эндпоинтам был доступ только у администраторов (user.role == admin)
Для этого создайте декоратор admin_required и декорируйте им  методы, которые нужно защитить.
`POST/PUT/DELETE`  /movies/ + /movies/id Authorized Required + Role admin Required

`POST/PUT/DELETE`  /genres/ + /genres/id Authorized Required + Role admin Required

POST/PUT/DELETE  /directors/ + /directors/id Authorized Required + Role admin Required

Шаг 7. Добавьте регистрацию пользователя
POST /users/ — создает пользовател Anonymous (кто угодно)

Пример запроса:
POST /users/

{
	"username": "ivan",
	"password": "qwerty",
	"role": "admin"
}

Шаг 8. Создайте  пользователей в БД
Создайте пользователей через запрос к api POST /users/, используя postman