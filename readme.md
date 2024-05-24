
# Project g_api
The g_api project is a repository that utilizes Python, FastAPI, SQL (PostgreSQL), PyDantic data search. It implements a CRUD application with JWT authentication for users, including user registration, login, and post creation. The application allows users to create posts search for posts, store them in the database with proper mapping and data types, and retrieve all searched data with unique identifiers. Additionally, it includes SQL table creation and retrieval based on user or post IDs.
## Setup Instructions

1. **Navigate to the project directory**:
   ```sh
   cd path/to/your/project
   ```

2. **Activate your virtual environment (if you're using one)**:
   ```sh
   .\env\Scripts\activate 
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
  4. **Install the dependencies**:
	   ```sh
		uvicorn main:app --reload
	   ```

## Accessing the API

To access the API, run the server and visit the following URLs:

- Base URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

### / (Root Endpoint)

- **Functionality**:
  - Displays a welcome message.
  - Redirects to other endpoints and documentation.

### /posts (Get All Posts)

- **Purpose**: Retrieve all posts from the database.
- **Functionality**:
  - Query all posts from the database.
  - Log the activity.

### /posts/{id} (Get Post by ID)

- **Purpose**: Retrieve a specific post by ID from the database.
- **Functionality**:
  - Query the database for the specified post.
  - Log the activity.

### /error (Error Endpoint)

- **Purpose**: Demonstrate error handling in the API.
- **Functionality**:
  - Throw an HTTP 400 error with a custom message.
  - Log the activity.

### /user/sign_up (User Sign-up)

- **Purpose**: Register a new user.
- **Functionality**:
  - Create a new user record in the database.
  - Log the activity.

### /user/login (User Login)

- **Purpose**: Authenticate a user and return a JWT token.
- **Functionality**:
  - Validate user credentials against database records.
  - Generate a JWT token for valid credentials.
  - Log the activity.
