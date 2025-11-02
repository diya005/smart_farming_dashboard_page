import streamlit as st
from pymongo import MongoClient

MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["smart_farming"]
users_collection = db["users"]
