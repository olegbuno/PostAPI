# PostAPI Application

This is a FastAPI post application for making posts by users.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone this repository:
  ```
  git clone https://github.com/your_username/your_repository.git
  ```
   
2. Navigate to the project directory:
  ```
  cd AssessmentSubmission
  ```

3. Usage
  ```
  docker-compose up --build
  ```

Go to http://127.0.0.1:8000/docs or http://localhost:8000/docs to see and test all the endpoints:
- Signup Endpoint:
    - Accepts `email` and `password`.
    - Returns a token (JWT or randomly generated string).
  

- Login Endpoint:
    - Accepts `email` and `password`.
    - Returns a token upon successful login; error response if login fails.


- AddPost Endpoint:
    - Accepts `text` and a `token` for authentication.
    - Validates payload size (limit to 1 MB), saves the post in memory, returning `postID`.
    - Returns an error for invalid or missing token.
    - Dependency injection for token authentication.


- GetPosts Endpoint:
    - Requires a token for authentication.
    - Returns all user's posts.
    - Implements response caching for up to 5 minutes for the same user.
    - Returns an error for invalid or missing token.
    - Dependency injection for token authentication.


- DeletePost Endpoint:
    - Accepts `postID` and a `token` for authentication.
    - Deletes the corresponding post from memory.
    - Returns an error for invalid or missing token.
    - Dependency injection for token authentication.