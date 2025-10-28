from pymongo import MongoClient

# ✅ Use your actual connection string (no quotes around variable name)
MONGO_URL = ""

# ✅ Connect to MongoDB Atlas
client = MongoClient(MONGO_URL)

# ✅ Select database and collection
db = client["testbook"]
collection = db["books"]

# ✅ Test the connection
try:
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

