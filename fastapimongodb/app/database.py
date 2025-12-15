from pymongo import MongoClient

MONGO_URL = "mongodb+srv://muhammadimran752310:admin123@cluster0.mwme6.mongodb.net/bookdb?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)
db = client["bookdb"]

users_collection = db["users"]
books_collection = db.get_collection("books")  # optional, if you use books
print("✅ MongoDB connection successful!")



# from pymongo import MongoClient

# # ✅ Use your actual connection string (no quotes around variable name)
# MONGO_URL = "mongodb+srv://muhammadimran752310:admin123@cluster0.mwme6.mongodb.net/fastapicrud?retryWrites=true&w=majority&appName=Cluster0"

# # ✅ Connect to MongoDB Atlas
# client = MongoClient(MONGO_URL)

# # ✅ Select database and collection
# db = client["testbook"]
# collection = db["books"]


# # Users collection (for register + login)
# users_collection = db["users"]

# # ✅ Test the connection
# try:
#     client.admin.command('ping')
#     print("✅ MongoDB connection successful!")
# except Exception as e:
#     print("❌ MongoDB connection failed:", e)

