from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import collection
from bson.objectid import ObjectId


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse )
def home(request: Request):
    books = list(collection.find())
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@router.get("/add", response_class=HTMLResponse)
def add_page(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@router.post("/add")
def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...)):
    collection.insert_one({"title": title, "author": author, "year": year})
    return RedirectResponse("/", status_code=303)

@router.get("/edit/{book_id}", response_class=HTMLResponse)
def edit_page(request: Request, book_id: str):
    book = collection.find_one({"_id": ObjectId(book_id)})
    return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})

@router.post("/edit/{book_id}")
def edit_book(book_id: str, title: str = Form(...), author: str = Form(...), year: int = Form(...)):
    collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"title": title, "author": author, "year": year}})
    return RedirectResponse("/", status_code=303)

@router.get("/delete/{book_id}")
def delete_book(book_id: str):
    collection.delete_one({"_id": ObjectId(book_id)})
    return RedirectResponse("/", status_code=303)
