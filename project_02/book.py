from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

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
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2025)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Coding With Ruby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2002,
            }
        }


def set_book_id(book: Book):
    """find last book id in the BOOKS list

    Args:
        book (Book): Book object

    Returns:
        Book object
    """

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


BOOKS = [
    Book(1, "Computer Science Pro", "CodeWithRuby", "A very nice book!", 5, 1999),
    Book(2, "Be Fast With FastAPI", "CodeWithRuby", "A great book!", 4, 1995),
    Book(3, "Master Endpoints", "CodeWithRuby", "A awesome book!", 5, 1995),
    Book(4, "HP1", "Author 1", "Book Description", 3, 2003),
    Book(5, "HP2", "Author 2", "Book Description", 1, 2003),
    Book(6, "HP3", "Author 3", "Book Description", 2, 2024),
]


@app.get("/books")
async def read_all_books():
    """return all books from BOOKS

    Returns:
        list: list of Book objects that shows as dictionary in the result.
    """
    return BOOKS


@app.get("/book/")
async def read_book_with_published_date(
    book_publish_date: int = Query(gt=1960, lt=2025),
):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == book_publish_date:
            books_to_return.append(BOOKS[i])

    return books_to_return


@app.get("/books/{book_id}")
async def read_book_with_id(book_id: int = Path(gt=0)):
    """return book base on id

    Args:
        book_id (int)

    Returns:
        Book object
    """
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found.")


@app.get("/books/")
async def read_book_with_rating(book_rating: int = Query(gt=-1, lt=6)):
    """return book base on specific rating

    Args:
        book_rating (int)

    Returns:
        list: list of books that has same rating.
    """
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)

    return book_to_return


@app.put("/books/book_update")
async def update_book(book_request: BookRequest):
    """update existing book base on book id

    Args:
        book_request (BookRequest): modified book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request
            return {"message": "Book was updated"}


@app.post("/create-book")
async def add_new_books(book_request: BookRequest):
    """create and add new book to BOOKS list

    Args:
        book_request (BookRequest)
    """
    new_book = Book(**book_request.model_dump())
    BOOKS.append(set_book_id(new_book))

    return {"message": "Book added"}


@app.delete("/delete-book")
async def delete_book(book_id: int = Query(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            break
