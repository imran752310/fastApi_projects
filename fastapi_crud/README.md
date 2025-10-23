# 🚀 FastAPI CRUD Application (Chai aur Code - No Database)

A simple **CRUD (Create, Read, Update, Delete)** API built using **FastAPI**, following the tutorial by [Chai aur Code](https://www.youtube.com/@chaiaurcode).  
This version uses **in-memory Python lists** instead of a database — perfect for beginners learning FastAPI basics.

---

## 📋 Features

- ✅ Create new items (POST)
- 📄 Read all items (GET)
- 🔍 Retrieve single item by ID (GET)
- ✏️ Update an item (PUT)
- ❌ Delete an item (DELETE)
- ⚡ Auto-generated Swagger UI and ReDoc documentation

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|----------|
| 🐍 **Python 3.11+** | Programming language |
| ⚡ **FastAPI** | Web framework for building APIs |
| 🚀 **Uvicorn** | ASGI server to run the FastAPI app |

---

## 📁 Project Structure


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/imran752310/fastapi-crud.git
cd fastapi-crud


python -m venv venv
source venv/bin/activate     # for macOS/Linux
venv\Scripts\activate        # for Windows

items = []

@app.post("/items/")
def create_item(item: Item):
    item.id = len(items) + 1
    items.append(item)
    return item
