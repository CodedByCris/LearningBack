from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='ID is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=6) # rating should be between 1 and 5
    published_date: int = Field(gt=1999, le=2025)
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Book Title',
                'author': 'Author Name',
                'description': 'Description of the book',
                'rating': 5,
                'published_date': 2023
            }
        },
    }

BOOKS = [
    Book(1, "Book One", "Author A", "Description of Book One", 5, 2020),
    Book(2, "Book Two", "Author A", "Description of Book Two", 5, 2020),
    Book(3, "Book Three", "Author A", "Description of Book Three", 5, 2021),
    Book(4, "Book Four", "Author D", "Description of Book Four", 2, 2021),
    Book(5, "Book Five", "Author E", "Description of Book Four", 1, 2022),
    Book(6, "Book Six", "Author F", "Description of Book Four", 3, 2022),
]

#!Getters

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/rating/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, le=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    if len(books_to_return) == 0:
        return {"error": "Book not found"}
    return books_to_return

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, le=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    if len(books_to_return) == 0:
        return {"error": "Book not found"}
    return books_to_return


#!Puts

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def upddate_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return BOOKS[i]
    raise HTTPException(status_code=404, detail="Book not found")

#!Posts

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_by_id(new_book))
    
def find_book_by_id(book: Book):    
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

#!Deletes

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")