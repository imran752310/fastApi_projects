from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import users_collection
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Password hashing
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simple session storage (for demo purposes)
sessions = {}

# ---------------- Register ----------------
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    if users_collection.find_one({"email": email}):
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Email already registered!"}
        )
    
    hashed_pw = pwd_ctx.hash(password)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw
    })
    return RedirectResponse("/login", status_code=303)

# ---------------- Login ----------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = users_collection.find_one({"email": email})
    if not user or not pwd_ctx.verify(password, user["password"]):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid credentials!"}
        )

    session_id = str(user["_id"])
    sessions[session_id] = user
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response

# ---------------- Dashboard ----------------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session_id: str = Cookie(None)):
    if session_id is None or session_id not in sessions:
        return RedirectResponse("/login")
    
    user = sessions[session_id]
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

# ---------------- Logout ----------------
@router.get("/logout")
def logout(session_id: str = Cookie(None)):
    if session_id in sessions:
        sessions.pop(session_id)
    response = RedirectResponse("/login")
    response.delete_cookie("session_id")
    return response


# from fastapi import APIRouter, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from app.database import users_collection
# from passlib.context import CryptContext
# from fastapi import Cookie

# router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")

# # Password hashing
# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Simple session storage (for demo purposes)
# sessions = {}

# # ---------------- Register ----------------
# @router.get("/register", response_class=HTMLResponse)
# def register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @router.post("/register")
# def register(
#     request: Request,
#     name: str = Form(...),
#     email: str = Form(...),
#     password: str = Form(...)
# ):
#     if users_collection.find_one({"email": email}):
#         return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered!"})
    
#     hashed_pw = pwd_ctx.hash(password)
#     users_collection.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_pw
#     })

#     return RedirectResponse("/login", status_code=303)

# # ---------------- Login ----------------
# @router.get("/login", response_class=HTMLResponse)
# def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/login")
# def login(
#     request: Request,
#     email: str = Form(...),
#     password: str = Form(...)
# ):
#     user = users_collection.find_one({"email": email})
#     if not user or not pwd_ctx.verify(password, user["password"]):
#         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials!"})

#     # Create a simple session
#     session_id = str(user["_id"])
#     sessions[session_id] = user
#     response = RedirectResponse("/dashboard", status_code=303)
#     response.set_cookie(key="session_id", value=session_id)
#     return response

# # ---------------- Dashboard ----------------
# @router.get("/dashboard", response_class=HTMLResponse)
# def dashboard(request: Request, session_id: str = Cookie(None)):
#     if session_id is None or session_id not in sessions:
#         return RedirectResponse("/login")
    
#     user = sessions[session_id]
#     return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

# # ---------------- Logout ----------------
# @router.get("/logout")
# def logout(session_id: str = Cookie(None)):
#     if session_id in sessions:
#         sessions.pop(session_id)
#     response = RedirectResponse("/login")
#     response.delete_cookie("session_id")
#     return response



# # from fastapi import APIRouter, Form, Request
# # from fastapi.responses import RedirectResponse
# # from passlib.context import CryptContext
# # from .database import users_collection

# # router = APIRouter()
# # pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # @router.get("/register")
# # async def register_page(request: Request):
# #     return request.app.state.templates.TemplateResponse(
# #         "register.html", {"request": request}
# #     )

# # @router.post("/register")
# # async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
# #     hashed_pw = pwd_ctx.hash(password)
    
# #     users_collection.insert_one({
# #         "name": name,
# #         "email": email,
# #         "password": hashed_pw
# #     })
    
# #     return RedirectResponse("/login", status_code=303)

# # @router.get("/login")
# # async def login_page(request: Request):
# #     return request.app.state.templates.TemplateResponse(
# #         "login.html", {"request": request}
# #     )

# # @router.post("/login")
# # async def login(email: str = Form(...), password: str = Form(...)):
# #     user = users_collection.find_one({"email": email})
    
# #     if not user:
# #         return RedirectResponse("/login", status_code=303)

# #     if not pwd_ctx.verify(password, user["password"]):
# #         return RedirectResponse("/login", status_code=303)

# #     return RedirectResponse("/dashboard", status_code=303)
