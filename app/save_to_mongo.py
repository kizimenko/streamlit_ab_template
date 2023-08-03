import pymongo
from pymongo import MongoClient
from datetime import datetime
import random
import string

import os

MONGODB_URI = os.environ.get("MONGODB_URI")
# Create a MongoDB client and connect to the database
client = MongoClient(MONGODB_URI)
db = client["test"]  # Replace "your_database_name" with your actual database name
collection = db["ideas"]  # Replace "ideas" with your desired collection name

def save_idea(idea_data):
    # Add the current timestamp for dateCreated and dateUpdated fields
    current_time = datetime.utcnow()
    idea_data["dateCreated"] = current_time
    idea_data["dateUpdated"] = current_time

    # Insert the idea data into the MongoDB collection
    result = collection.insert_one(idea_data)
    if result.acknowledged:
        print("Idea inserted successfully with ID:", result.inserted_id)
    else:
        print("Failed to insert idea.")

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_idea_id():
    random_string = generate_random_string(15) 
    return f"idea_{random_string}"




def make_idea_body(title,ice,details,project):
    project = project.lower()
    project_dicts = {
        'mostbet':'prj_eevpg1olkvhywr4',
        'betandreas':'prj_eevpg1mlkmgo2fk',
        'bivi':'prj_eevpg1olkvhz17c',
    }
    idea_id = generate_idea_id()  

    idea = {
    "id": idea_id,
    "text": title,
    "archived": False,
    "userId": "u_eevpg1tlgmilc36",
    "organization": "org_eevpg1tlgmilj1j",
    "project": f'{project_dicts[project]}',
    "tags": [f"ICE:{ice}"],
    "votes": [],
    "experimentLength": 7,
    "details":details,
    }
    return idea,idea_id

