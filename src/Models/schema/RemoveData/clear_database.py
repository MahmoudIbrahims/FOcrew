import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('/mnt/c/Users/M/Desktop/FOcrew/src/.env')

async def clear_tables():
    # Get database credentials from environment
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_MAIN_DATABASE = os.getenv("POSTGRES_MAIN_DATABASE")
    
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_MAIN_DATABASE}"
    
    print(f"Connecting to: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_MAIN_DATABASE}")
    
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.begin() as conn:
        print("Clearing tables...")
        await conn.execute(text("DROP TABLE IF EXISTS user_files CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS projects CASCADE;"))
        await conn.execute(text("DELETE FROM alembic_version;"))
        print("Done! Tables dropped.")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(clear_tables())