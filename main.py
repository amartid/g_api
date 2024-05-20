import uvicorn
from fastapi import FastAPI, Body, HTTPException, Depends
from starlette.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from database.database import SessionLocal, init_db
from database.models import Post, User
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT, extract_jwt_username
from app.auth.jwt_bearer import JWTBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import time
# Create a FastAPI "instance"
app = FastAPI()

# Dependency to get the DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    await init_db()



# Configure logging
def configure_logger():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    log_filename = f"app_{time.strftime('%Y%m%d_%H%M%S')}.log"  # Append timestamp to log filename
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

logger = configure_logger()

# Test log message
logger.info("Application started")

@app.get("/", tags=["test"], response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
    <head>
        <title>Root</title>
    </head>
    <body>
        <h1>Welcome to the Geodata API!</h1>
        <p>This is an HTML representation of the root endpoint.</p>
        <p><a href="/docs">Click here to go to the documentation</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/posts", tags=["posts"])
async def get_posts(db: AsyncSession = Depends(get_db)):
    logger.info("Posts endpoint called")
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts

@app.get("/posts/{id}", tags=["posts"])
async def get_post(id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Post/{id} endpoint called")
    result = await db.execute(select(Post).filter(Post.id == id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/error")
async def error_endpoint():
    logger.error("Error endpoint called")
    raise HTTPException(status_code=400, detail="This is a sample error")

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def create_post(post: PostSchema, jwt_token: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    # Get the username from the JWT token
    username = extract_jwt_username(jwt_token)

    # Find the user by username
    result = await db.execute(select(User).filter(User.email == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the new post and associate it with the user
    new_post = Post(title=post.title, text=post.text, owner_id=user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return {"message": "Post created successfully", "post_id": new_post.id}

@app.post("/user/sign_up", tags=["user"])
async def create_user(user: UserSchema = Body(default=None), db: AsyncSession = Depends(get_db)):
    """
    Registers a new user.
    :param user: The user data.
    :param db: The database session.
    :return: A JWT token for the newly created user.
    """
    logger.info("User sign-up endpoint called for email: %s", user.email)
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    logger.info(f"User created successfully with email: {user.email}")
    return signJWT(user.email)

async def check_user(data: UserLoginSchema, db: AsyncSession):
    """
    Validates user credentials.
    :param data: The login data.
    :param db: The database session.
    :return: A status indicating whether the credentials are valid.
    """
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalar_one_or_none()
    
    if user:
        if user.password == data.password:
            return {"status": True, "message": "Valid credentials"}
        else:
            return {"status": False, "message": "Invalid password"}
    else:
        return {"status": False, "message": "User does not exist"}

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token.
    :param user: The login data.
    :param db: The database session.
    :return: A JWT token if the credentials are valid.
    """
    logger.info("User login endpoint called for email: %s", user.email)
    check_result = await check_user(user, db)
    
    if check_result["status"]:
        logger.info("User authenticated successfully: %s", user.email)
        return signJWT(user.email)
    else:
        logger.warning("User authentication failed for email: %s. Reason: %s", user.email, check_result["message"])
        raise HTTPException(status_code=401, detail=check_result["message"])

@app.get("/user/{user_id}/posts", tags=["posts"])
async def get_user_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve posts by user ID.
    :param user_id: The ID of the user.
    :param db: The database session.
    :return: A list of posts associated with the user.
    """
    logger.info(f"Fetching posts for user ID: {user_id}")
    
    # Query the database for posts associated with the user ID
    result = await db.execute(select(Post).filter(Post.owner_id == user_id))
    posts = result.scalars().all()
    
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    
    return posts

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)











'''
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def create_post(post: PostSchema, jwt_token: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)):
    # Get the username from the JWT token
    username = JWTBearer.extract_jwt_username(jwt_token)

    # Find the user by username
    user = await db.execute(select(User).filter(User.username == username))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the new post and associate it with the user
    new_post = Post(title=post.title, text=post.text, owner_id=user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return {"message": "Post created successfully", "post_id": new_post.id}

@app.post("/user/sign_up", tags=["user"])
async def create_user(user: UserSchema = Body(default=None), db: AsyncSession = Depends(get_db)):
    logger.info("User sign-up endpoint called")
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return signJWT(user.email)

async def check_user(data: UserLoginSchema, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalar_one_or_none()
    if user:
        if user.password == data.password:
            return {"status": True, "message": "Valid credentials"}
        else:
            return {"status": False, "message": "Invalid password"}
    else:
        return {"status": False, "message": "User does not exist"}

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...), db: AsyncSession = Depends(get_db)):
    logger.info("User login endpoint called")
    check_result = await check_user(user, db)
    if check_result["status"]:
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail=check_result["message"])
'''