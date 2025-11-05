from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DATABASE_URL = "sqlite+aiosqlite:///./movieticketbooking.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() :
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(f"Error occurred: {e}")
        finally:
            await session.commit()
            await session.close()


