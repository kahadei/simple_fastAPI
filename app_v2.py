from typing import Optional

from books import BOOKS
from fastapi import FastAPI
from dataclasses import dataclass
from pydantic import BaseModel, Field

app = FastAPI()


@dataclass
class Book:
    id: int
    title: str
    author: str
    descript: str
    rating: float
    year: int


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='ID is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    descript: str = Field(min_length=3, max_length=300)
    rating: float = Field(gt=-1, lt=10.0)
    year: int = Field(gt=1900, lt=2050)

    class Config:
        json_schema_extra = {
            'example': {'title': 'A new book',
                        'author': 'kahadei.com',
                        'descript': 'Stand with Ukraine',
                        'rating': 5,
                        'year': 2022}
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get('/')
async def first_api():
    return {'message': 'Hello, reader'}


@app.get('/books')
async def books():
    return BOOKS


@app.get('/books/')
async def fetch_by_rating(book_rating: float):
    books_by_rating = []
    for book in BOOKS:
        if book.rating >= book_rating:
            books_by_rating.append(book)
    return books_by_rating


@app.post('/books/add_new')
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(assigment_book_id(new_book))


def assigment_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put('/books/update_books')
async def book_update(book_search: BookRequest):
    for i, book in enumerate(BOOKS):
        if book.id == book_search.id:
            BOOKS[i] = book_search


@app.delete('/books/delete_book/{del_book}')
async def update_book(book_id: int):
    for i, book in enumerate(BOOKS):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
