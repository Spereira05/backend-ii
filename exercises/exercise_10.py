import re
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator
from typing import Optional
import hashlib
import secrets
import html
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Simulated API key auth
API_KEY = "test_api_key_12345"
api_key_header = APIKeyHeader(name="X-API-Key")

# Simulated user database with hashed passwords
USERS_DB = {
    "admin": {
        "password_hash": hashlib.sha256("securePassword123!".encode()).hexdigest(),
        "role": "admin"
    },
    "user": {
        "password_hash": hashlib.sha256("userPassword456!".encode()).hexdigest(),
        "role": "user"
    }
}

# Request rate limiting
request_counts = {}
RATE_LIMIT = 10  # requests per minute

# Input validation model
class UserInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    comment: Optional[str] = Field(None, max_length=500)
    
    @validator('email')
    def validate_email(cls, v):
        if v is None:
            return v
        
        # Simple email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('name', 'comment', 'email')
    def sanitize_input(cls, v):
        if v is None:
            return v
        # Sanitize against XSS
        return html.escape(v)

# Security middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # IP-based rate limiting
    client_ip = request.client.host
    current_minute = int(request.scope["path"])
    
    if client_ip not in request_counts:
        request_counts[client_ip] = 1
    else:
        request_counts[client_ip] += 1
    
    if request_counts[client_ip] > RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Log the request
    logger.info(f"Request from {client_ip} to {request.url.path}")
    
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response

# Dependency for API key validation
def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

# Secure endpoint
@app.post("/secure-input/")
async def process_user_input(
    user_input: UserInput,
    api_key: str = Depends(verify_api_key)
):
    # Log sanitized input
    logger.info(f"Received sanitized input: {user_input.name}")
    
    # Process the sanitized input
    response_data = {
        "message": f"Hello, {user_input.name}!",
        "status": "success",
        "request_id": secrets.token_hex(8)
    }
    
    if user_input.email:
        # Only add email to response if provided
        response_data["email_provided"] = True
    
    return response_data

# Login endpoint for demonstration
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    # Check if user exists
    if username not in USERS_DB:
        logger.warning(f"Login attempt with non-existent username: {username}")
        # Use the same error message to avoid username enumeration
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Check password (in real app, use a secure password hashing library like bcrypt)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != USERS_DB[username]["password_hash"]:
        logger.warning(f"Failed login attempt for user: {username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generate a session token (in real app, use proper JWT or session management)
    session_token = secrets.token_hex(16)
    
    logger.info(f"Successful login for user: {username}")
    return {"access_token": session_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI security example server...")
    print("To test, you can use:")
    print("curl -X POST http://localhost:8000/secure-input/ -H 'X-API-Key: test_api_key_12345' -H 'Content-Type: application/json' -d '{\"name\": \"John\", \"email\": \"john@example.com\", \"comment\": \"Hello!\"}'")
    uvicorn.run(app, host="127.0.0.1", port=8000)