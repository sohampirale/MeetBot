from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
import os


async def init_database():
    """Initialize MongoDB connection and Beanie ODM."""
    try:
        # Get MongoDB URL from environment or use default
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "meetbot")

        # Create MongoDB client
        client = AsyncIOMotorClient(mongodb_url)

        # Initialize Beanie with models
        await init_beanie(database=client[database_name], document_models=[User])

        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        raise
