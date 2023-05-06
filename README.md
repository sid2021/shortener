# Using the project in local environment

1. Clone the repository.
2. Run the following commands:

```bash
cd docker
chmod +x docker-entrypoint.sh
docker-compose build
docker-compose up
```

In second terminal run this command to create superuser.
```
docker-compose exec web python manage.py createsuperuser
```

Access Django app container shell:
```
docker exec -it url_shortener /bin/bash
```

To play with psql use:
```
docker-compose exec db psql --username=devel --dbname=shortener
\c shortener
\dt
\q
```

3. Check if project is successfully running by going into `http://localhost:8001/admin/` (use username/password generated in step 2 above) or `http://localhost:8001/swagger/`.
4. We are using Django Rest Framework's `TokenAuthentication`. In order to generate token necessary to send correct header within each request use the following commnands:
```bash
docker-compose exec web python manage.py shell
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
u = get_user_model().objects.first()
token = Token.objects.create(user=u)
```

Copy the token obtained above to the authorization header which should look like that:

```
Authorization: Token <token>
```

5. After the process is complete send `POST` and `GET `requests to the following endpoints:

```
POST http://localhost:8001/api/v1/get-short/ # Get shortened URL
POST http://localhost:8001/api/v1/get-full/ # Get full URL
GET http://localhost:8001/api/v1/get-urls/ # Get list of all URLs
```

Make sure that you provide correct TokenAuthentication credentials (refer to step 4 above).

## Running tests locally

```
cd docker
docker-compose run --rm web test
```

# Main libraries used to build the project

- django
- djangorestframework
- drf-yasg
- psycopg2-binary
- dj-database-url
- pip-tools
- pytest

# API Documentation

API documentation is available at `http://localhost:8001/swagger/`.

# Requests examples

Examples of http requests using `requests` library were provided below. Make sure to use correct token.

Get shortened URL

```python
import requests
import json

url = "http://localhost:8001/api/v1/get-short/"

payload = json.dumps({
  "url": "https://www.google.com"
})
headers = {
  'Authorization': 'Token <token>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Get full URL

```python
import requests
import json

url = "http://localhost:8001/api/v1/get-full/"

payload = json.dumps({
  "url": "http://foobar.com/39b39250d1350fd6b8df06821f81da3c"
})
headers = {
  'Authorization': 'Token <token>',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Get list of all URLs

```python
import requests
import json

url = "http://localhost:8001/api/v1/get-urls/"

payload = ""
headers = {
  'Authorization': 'Token <token>',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```


# Postman collection

For conveniance a Postman collection was provided in the app's root directory (`postman_collection.json`).

# Production environment

No settings for production environment were implemented. App was configured for local development only.
