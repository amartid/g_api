from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Update the SQLAlchemy database URL for PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/geodata"

# Create a SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session local class with the async engine
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Create a base class for SQLAlchemy models
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # Reflect existing tables
        existing_tables = await conn.run_sync(Base.metadata.reflect)

        # Check if any tables exist
        if not existing_tables:
            # If no tables exist, create all tables
            await conn.run_sync(Base.metadata.create_all)
        else:
            # If tables exist, continue without dropping and recreating
            print("Database tables already exist. Skipping creation.")
