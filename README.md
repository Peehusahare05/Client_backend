# Stateless JWT Authentication System

A robust, stateless authentication system built with **FastAPI**, **MongoDB**, and **JWT** (Access & Refresh tokens).

## Features
- **Stateless**: No sessions stored on the server.
- **Refresh Tokens**: Automatically issue new access tokens.
- **Secure**: Password hashing with `bcrypt` (Salted).
- **Easy Testing**: Includes Postman-ready examples.

## Prerequisites
- Python 3.9+
- Local MongoDB running at `mongodb://localhost:27017`

## Setup Instructions

1. **Clone the project & Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Check `.env` file for database and JWT secret configurations.

3. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

---

## API Endpoints & Postman Examples

### 1. Register User
- **URL**: `http://127.0.0.1:8000/auth/register`
- **Method**: `POST`
- **Body (JSON)**:
```json
{
    "username": "peehuthequeen",
    "email": "peehu@example.com",
    "password": "strongpassword123"
}
```

### 2. Login
- **URL**: `http://127.0.0.1:8000/auth/login`
- **Method**: `POST`
- **Body (JSON)**:
```json
{
    "email": "peehuthequeen@example.com",
    "password": "strongpassword123"
}
```
*Note: This returns an `access_token` and a `refresh_token`.*

### 3. Refresh Token
- **URL**: `http://127.0.0.1:8000/auth/refresh?refresh_token={{refresh_token}}`
- **Method**: `POST`
- **Params**: 
  - `refresh_token`: (Paste the refresh token received from login)

### 4. Protected Route (Get Me)
- **URL**: `http://127.0.0.1:8000/auth/me`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Bearer {{access_token}}`

---

## Interactive Docs
Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
"# Client_backend" 
"# Private__project" 
"# Private__project" 
