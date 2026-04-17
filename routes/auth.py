from fastapi import APIRouter, HTTPException, status
from models.user import UserRegister, UserLogin, TokenResponse
from database import users_collection
from utils.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(user: UserRegister):
    # Check if username already exists
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email already exists
    existing_email = await users_collection.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Save new user
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password)
    }
    await users_collection.insert_one(new_user)
    return {"message": "User registered successfully!"}

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token, username=user.username)

@router.get("/me")
async def get_me(username: str):
    """Get user profile (pass username as query param for demo)"""
    user = await users_collection.find_one({"username": username}, {"hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user
