from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from bson.objectid import ObjectId
from app.database import collection, users


from app.database import collection, users

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- Authentication Helpers ----------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


# ---------------- Home (Protected) ----------------~

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.cookies.get("user")

    books = list(collection.find())

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "books": books,
            "user": user
        }
    )




# ---------------- Register ----------------

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if users.find_one({"email": email}):
        response = templates.TemplateResponse(
            "register.html",
            {"request": {}, "error": "Email already exists!"}
        )
        return response

    # hashed = hash_password(password)

    users.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return RedirectResponse("/login", status_code=303)


# ---------------- Login ----------------

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users.find_one({"email": email})

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Email does not exist!"}
        )

    if not verify_password(password, user["password"]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Incorrect password!"}
        )

    response = RedirectResponse("/", status_code=303)
    response.set_cookie("user", user["email"])
    return response


# ---------------- Logout ----------------

@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user")
    return response


# ---------------- ADD Page (Login Required) ----------------

@router.get("/add", response_class=HTMLResponse)
def add_page(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("add_book.html", {"request": request})


@router.post("/add")
def add_book(request: Request, title: str = Form(...), author: str = Form(...), year: int = Form(...)):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    collection.insert_one({"title": title, "author": author, "year": year})
    return RedirectResponse("/", status_code=303)


# ---------------- Edit Book (Login Required) ----------------

@router.get("/edit/{book_id}", response_class=HTMLResponse)
def edit_page(request: Request, book_id: str):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    book = collection.find_one({"_id": ObjectId(book_id)})
    return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})


@router.post("/edit/{book_id}")
def edit_book(request: Request, book_id: str, title: str = Form(...), author: str = Form(...), year: int = Form(...)):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"title": title, "author": author, "year": year}})
    return RedirectResponse("/", status_code=303)


# ---------------- Delete Book (Login Required) ----------------

@router.get("/delete/{book_id}")
def delete_book(request: Request, book_id: str):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    collection.delete_one({"_id": ObjectId(book_id)})
    return RedirectResponse("/", status_code=303)


# from fastapi import APIRouter, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from app.database import collection
# from bson.objectid import ObjectId


# router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")

# @router.get("/", response_class=HTMLResponse )
# def home(request: Request):
#     books = list(collection.find())
#     return templates.TemplateResponse("index.html", {"request": request, "books": books})

# @router.get("/add", response_class=HTMLResponse)
# def add_page(request: Request):
#     return templates.TemplateResponse("add_book.html", {"request": request})

# @router.post("/add")
# def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...)):
#     collection.insert_one({"title": title, "author": author, "year": year})
#     return RedirectResponse("/", status_code=303)

# @router.get("/edit/{book_id}", response_class=HTMLResponse)
# def edit_page(request: Request, book_id: str):
#     book = collection.find_one({"_id": ObjectId(book_id)})
#     return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})

# @router.post("/edit/{book_id}")
# def edit_book(book_id: str, title: str = Form(...), author: str = Form(...), year: int = Form(...)):
#     collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"title": title, "author": author, "year": year}})
#     return RedirectResponse("/", status_code=303)

# @router.get("/delete/{book_id}")
# def delete_book(book_id: str):
#     collection.delete_one({"_id": ObjectId(book_id)})
#     return RedirectResponse("/", status_code=303)





# # from fastapi import APIRouter, Request, Form
# # from fastapi.responses import HTMLResponse, RedirectResponse
# # from fastapi.templating import Jinja2Templates
# # from app.database import collection
# # from bson.objectid import ObjectId


# # router = APIRouter()
# # templates = Jinja2Templates(directory="app/templates")

# # @router.get("/", response_class=HTMLResponse )
# # def home(request: Request):
# #     books = list(collection.find())
# #     return templates.TemplateResponse("index.html", {"request": request, "books": books})

# # @router.get("/add", response_class=HTMLResponse)
# # def add_page(request: Request):
# #     return templates.TemplateResponse("add_book.html", {"request": request})

# # @router.post("/add")
# # def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...)):
# #     collection.insert_one({"title": title, "author": author, "year": year})
# #     return RedirectResponse("/", status_code=303)

# # @router.get("/edit/{book_id}", response_class=HTMLResponse)
# # def edit_page(request: Request, book_id: str):
# #     book = collection.find_one({"_id": ObjectId(book_id)})
# #     return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})

# # @router.post("/edit/{book_id}")
# # def edit_book(book_id: str, title: str = Form(...), author: str = Form(...), year: int = Form(...)):
# #     collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"title": title, "author": author, "year": year}})
# #     return RedirectResponse("/", status_code=303)

# # @router.get("/delete/{book_id}")
# # def delete_book(book_id: str):
# #     collection.delete_one({"_id": ObjectId(book_id)})
# #     return RedirectResponse("/", status_code=303)
