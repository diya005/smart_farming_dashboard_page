from pymongo import MongoClient

# Your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://diyatheyashery_db_user:s05dKShUEPZrGxTu@cluster0.tli7vn0.mongodb.net/?appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client["smart_farming"]             # database name
users_collection = db["users"]           # collection name for users
