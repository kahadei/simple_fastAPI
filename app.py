from books import BOOKS
from fastapi import FastAPI, Body


app = FastAPI()


@app.get('/')
async def first_api():
    return {'message': 'Hello, reader'}


@app.get('/books')
async def books():
    return BOOKS


@app.get('/books/{book_title}')
async def read_book(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get('/books_by/')
async def books_by_author_category(category: str, author: str = 'Author One'):
    books_by_category = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and book.get('author').casefold() == author.casefold():
            books_by_category.append(book)
    return books_by_category


@app.post('/books/create_new')
async def post_new_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book(update_book=Body()):
    for i, book in enumerate(BOOKS):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i].update(update_book)


@app.delete('/books/delete_book/{del_book}')
async def update_book(del_book:str):
    for i, book in enumerate(BOOKS):
        if BOOKS[i].get('title').casefold() == del_book.casefold():
            BOOKS.pop(i)
