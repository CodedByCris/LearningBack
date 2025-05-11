from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "Book 1", "author": "Author 1", "category": "Fiction"},
    {"title": "Book 2", "author": "Author 2", "category": "Non-Fiction"},
    {"title": "Book 3", "author": "Author 3", "category": "Science"},
    {"title": "Book 4", "author": "Author 4", "category": "Fiction"},
    {"title": "Book 5", "author": "Author 5", "category": "Fiction"},
    {"title": "Book 6", "author": "Author 2", "category": "Science"},
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#@app.get("/books/mybook")
#async def get_my_book():
#    return {"title": "My Book", "author": "Me"}

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("books/byauthor/")
async def read_author_by_query(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(book = Body()):
    BOOKS.append(book)
    return book

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
