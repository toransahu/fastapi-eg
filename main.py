#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2020-02-28 14:43

"""Main."""


from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


app = FastAPI()

books = [
    {
        "name": "Book1",
        "price": 100,
        "isbn": 12345001
    },
    {
        "name": "Book2",
        "price": 200,
        "isbn": 12345002
    },
]


@app.get("/")
def hello():
    return {"Hello": "World!"}


@app.get("/books")
def get_books():
    """GET /books"""
    return {"books": books}


@app.get("/books/{isbn}")
def get_book_by_isbn(isbn: int):
    """GET /books/12345001"""
    for book in books:
        if book.get("isbn") == isbn:
            return book
    return JSONResponse({"error": "Book with ISBN %s not found." % isbn}, status_code=HTTP_404_NOT_FOUND)


def is_valid_book(book):
    if "name" in book and "isbn" in book and "price" in book:
        return True
    return False


@app.post("/books", status_code=HTTP_201_CREATED)
def add_book(book: dict):
    """POST /books
    {
        "name": "Some Book",
        "isbn": 12345009,
        "price": 900
    }

    """
    for _book in books:
        if _book.get("isbn") == book.get("isbn"):
            return JSONResponse(content={"error": "Book already exists."}, status_code=400)
    if is_valid_book(book):
        books.append(book)
        return book
    return JSONResponse(content={"error": "Invalid book."}, status_code=400)


@app.put("/books/{isbn}", status_code=HTTP_200_OK)
def update_book(isbn: int, book: dict):
    """PUT /books/12345001
    {
        "name": "Some book v2",
        "price": 150,
        "isbn": 12345008
    }
    """

    for _book in books:
        if _book["isbn"] == isbn:
            break

    if not updated_book:
        return JSONResponse({"error": "Book with ISBN %s not found." % isbn}, status_code=HTTP_404_NOT_FOUND)

    _book = book  # replace price & name
    res = JSONResponse(content=_book)
    res.headers["Location"] = "/books/" + str(isbn)
    return res


@app.patch("/books/{isbn}", status_code=HTTP_200_OK)
def partial_update_book(isbn: int, book: dict):
    """PATCH /books/12345001
    {
        "price": 150
    }
    """

    updated_book = None
    for _book in books:
        if _book["isbn"] == isbn:
            updated_book = _book

    if not updated_book:
        return JSONResponse({"error": "Book with ISBN %s not found." % isbn}, status_code=HTTP_404_NOT_FOUND)

    updated_book.update(book)
    res = JSONResponse(content=updated_book)
    res.headers["Location"] = "/books/" + str(isbn)
    return res


@app.delete("/books/{isbn}", status_code=HTTP_204_NO_CONTENT)
def delete_book(isbn: int):
    """DELETE /books/12345001"""

    global books
    for idx, _book in enumerate(books):
        if _book["isbn"] == isbn:
            books = books[:idx] + books[idx+1:]
            return
    return JSONResponse({"error": "Book with ISBN %s not found." % isbn}, status_code=HTTP_404_NOT_FOUND)
