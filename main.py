#python -m uvicorn main:app --reload
#aboba
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson import ObjectId

# create FastAPI app
app = FastAPI()


# connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["users_db"]
users_collection = db["users"]


# Model User
class User(BaseModel):
    #id: Optional[str] = None
    name: str
    age: int


    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Artem",
    #             "age": "21"
    #         }
    #     }



#region CRUD endpoints


# get User ID
@app.get("/user/id/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"id": str(user["_id"]), "name": user["name"], "age": user["age"]}
    raise HTTPException(status_code=404, detail="User not found")


# save User
@app.post("/user/save")
async def save_user(user: User):
    result = users_collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}


# update User Data
@app.put("/user/update/{user_id}")
async def update_user(user_id: str, user: User):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user.dict(exclude_unset=True)}
    )
    if result.matched_count:
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")



# delete User
@app.delete("/user/delete/{user_id}")
async def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")