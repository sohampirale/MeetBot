from fastapi import APIRouter, HTTPException, status, Response
from models.schemas import UserSignupRequest, UserAuthResponse, UserSigninRequest
from models.user import User
from helpers.password import hash_password, verify_password
from helpers.jwt import create_access_token, create_session_token
from database import init_database

router = APIRouter(prefix="/api/v1/user", tags=["user"])


@router.post(
    "/signup", response_model=UserAuthResponse, status_code=status.HTTP_201_CREATED
)
async def signup(user_data: UserSignupRequest, response: Response):
    """Create a new user account and return authentication tokens."""
    try:
        # Normalize input
        normalized_username = user_data.username.lower().strip()
        normalized_email = user_data.email.lower().strip()

        # Check if user already exists
        existing_user_by_email = await User.find_one(User.email == normalized_email)
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists with this email",
            )

        existing_user_by_username = await User.find_one(
            User.username == normalized_username
        )
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists with this username",
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create new user
        new_user = User(
            username=normalized_username,
            email=normalized_email,
            password=hashed_password,
        )

        await new_user.save()

        # Create JWT tokens
        token_payload = {
            "userId": str(new_user.id),
            "email": new_user.email,
            "username": new_user.username,
        }

        access_token = create_access_token(token_payload)
        refresh_token = create_session_token(token_payload)

        # Set cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=86400,  # 1 day
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=864000,  # 10 days
        )

        return UserAuthResponse(message="Signup successful", userId=str(new_user.id))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/signin", response_model=UserAuthResponse)
async def signin(user_data: UserSigninRequest, response: Response):
    """Authenticate a user and return authentication tokens."""
    try:
        # Validate input
        if not user_data.username and not user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either username or email must be provided",
            )

        # Find user by username or email
        user = None
        lookup_field = None

        if user_data.username:
            normalized_username = user_data.username.lower().strip()
            user = await User.find_one(User.username == normalized_username)
            lookup_field = "username"
        elif user_data.email:
            normalized_email = user_data.email.lower().strip()
            user = await User.find_one(User.email == normalized_email)
            lookup_field = "email"

        # Check if user exists
        if not user:
            field_name = "username" if lookup_field == "username" else "email"
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found with this {field_name}",
            )

        # Verify password
        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        # Create JWT tokens
        token_payload = {
            "userId": str(user.id),
            "email": user.email,
            "username": user.username,
        }

        access_token = create_access_token(token_payload)
        refresh_token = create_session_token(token_payload)

        # Set cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=86400,  # 1 day
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=864000,  # 10 days
        )

        return UserAuthResponse(message="Sign-in successful", userId=str(user.id))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
