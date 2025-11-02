from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://diyatheyashery_db_user:s05dKShUEPZrGxTu@cluster0.tli7vn0.mongodb.net/?appName=Cluster0"

# Connect to MongoDB Atlas
try:
    client = MongoClient(MONGO_URI)
    db = client["smart_farming"]
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("❌ Connection failed:", e)
