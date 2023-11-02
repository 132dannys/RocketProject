![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Celery](https://img.shields.io/badge/celery-37814A.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)

# What's Rocket repository?

Its a test task repository of Chain Objects system application.

---

## How to start
First of all configurate [dev.env](https://github.com/132dannys/RocketProject/blob/main/api/dev.env) file. Change email env to your own.

- Build project
```sh
  cd api
```
```sh
  docker compose build
```
- Run migrations
```sh
    make container-django-shell
```
```sh
    python manage.py makemigrations
```
```sh
    python manage.py migrate
```
- You can also fill the database with demo data. In **api** directory run django shell:
```sh
    make container-django-shell
```
```sh
    python manage.py demo_db
```
- Create superuser
```sh
    make container-django-shell
```
```sh
    python manage.py createsuperuser
```
- Run application
```sh
  docker compose up
```

## Local Development
Install *pre-commit*
```sh
    pre-commit install
```

## Usage

Application will be available via this link http://localhost:8000/objects/.
Access to API can get only *active* users.

### Available API routes:
You can check all routes using swagger(http://localhost:8000/api/v1/swagger/) or redoc(http://localhost:8000/api/v1/)

***Common links***:

**Auth:**
Authentication provides by using JWT.

- http://localhost:8000/auth/user/. Method **POST**: New user registration.
- http://localhost:8000/auth/jwt/create/. Method **POST**: Login as user, returns the generated JWT.
You can check other Auth module link in autodocumentation.

**Admin Panel:**
- http://localhost:8000/admin/.
It provides deleting Debt for selected Object, filter by City and link to Supplier. And other default admin staff.

**Objects:**
Object Model provide validation by hierarchy.
*Each Object in the Chain refers to only one equipment supplier (not
necessarily the previous one in the hierarchy). It is important to note that the hierarchy level
is determined not by the name of the link, but by its relationship to other Object of the Chain, i.e.
the Factory is always at level 0, and if the Retail relates directly to
Factory, bypassing other links - its level is 1.*

- http://localhost:8000/api/v1/objects/. Method **GET**: get all Objects data. Method **POST**: create new object.
Also you can filter data by City and Product(*uuid*) using query params:
``http://localhost:8000/api/v1/objects/?city=Brest&product={product.uuid}
``
- http://localhost:8000/api/v1/objects/{object.uuid}/. Methods **PUT, PATCH , DELETE**.
You can change or delete Object by its *uuid*. Dont allow you to change Debt by API.

- http://localhost:8000/api/v1/objects/object_statistic/. Method **GET**: Get Objects, where Debt more than average Debt in Chain.

- http://localhost:8000/api/v1/objects/send_email/. Method **POST**: Accepts uuid of Object. You will get email with QR code which consists information about with Object.

**Products:**
Product model provide validation: Release date cannot be date before today.

- http://localhost:8000/api/v1/producs/. Method **GET**: get all Products data.

- http://localhost:8000/api/v1/producs/{product.uuid}. Methods **PUT, PATCH , DELETE**.
You can change or delete Product by its *uuid*.

***Secure link***:
http://localhost:8000/api/v1/secure_objects/. Method **GET**. User can get information only about its own Object.

### Celery

API consist 2 schedule celery task:
- decrease_debt(), which runs every day at 6:30am and decrease debt y random value (100, 10000).
- increase_debt(), which runs every 3 hours and increase debt y random value (5, 500).

When you are deleting more than 20 debts in admin panel it starts celery task.
Sending emails also providing by celery task.
