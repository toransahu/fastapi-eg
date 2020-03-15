# Explore REST API Using FastAPI

```
GET /books  200

POST /books  201
{
    "name": "Some Book",
    "price": 120,
    "isbn": 12345001
}

GET /books/<isbn>  200

PUT /books/<isbn>  200
{
    "name": "New Name",
    "price": 200
}

PATCH /books/<isbn>  200
{
    "price": 300
}

DELETE /books/<isbn>  204
```

# Links
- https://pyvideo.org/pycon-india-2015/rest-apis-what-why-and-how-pycon-india-2015.html
