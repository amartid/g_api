import uvicorn
from fastapi import FastAPI,Body, HTTPException, Depends
from app.model import PostSchema
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer
import asyncio
import logging

# Run the development server (like uvicorn main:app --reload).

# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Create a FastAPI "instance"
app = FastAPI()


posts = [
    {
        "id": 1,
        "title": "Penguins 🐧 ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers 🐯 ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas 🐨",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },
]

users = []

# Get - for testing
@app.get("/", tags = ["test"]) # The Homepage
async def root():
    logger.info("Root endpoint called")
    return {"message": "This is geodata API"}

# Get Posts
@app.get("/posts", tags = ["posts"]) # The Homepage
async def get_posts():
    logger.info("Posts endpoint called")
    return posts

# Get single post {id}
@app.get("/posts/{id}", tags = ["posts"]) # The Homepage
async def get_post(id: int):
    logger.info("Post/{id} endpoint called")
    if id > len(posts):
        return{"error": "Post not found"}
    for post in posts:
        if post["id"] == id:
            return {
                "data": post}
        
# Handler for creating a post
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def create_post(post: PostSchema):
    logger.info("Post endpoint called")

    # Assign an id to the new post
    post.id = len(posts) + 1
    
    # Append the post to the list
    posts.append(post.dict())
    
    return {"data": "Post Added successfully"}


# User sign-up endpoint
@app.post("/user/sign_up", tags=["user"])
async def create_user(user: UserSchema = Body(default=None)):
    logger.info("User sign-up endpoint called")
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

# User login endpoint
@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    logger.info("User login endpoint called")
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/error")
async def error_endpoint():
    logger.error("Error endpoint called")
    raise HTTPException(status_code=400, detail="This is a sample error")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
