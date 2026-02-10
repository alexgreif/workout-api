import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.core.database import get_db
from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture(autouse=True)
def clean_database():
    with engine.begin() as conn:
        conn.execute(text("""
            TRUNCATE TABLE
                exercise_muscles,
                exercises,
                users
            RESTART IDENTITY CASCADE
        """))
    yield


@pytest.fixture()
def db_session():
    with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
def client(db_session):
    app = create_app()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def muscle_ids_by_name(client):
    response = client.get("/muscles/")
    muscles = response.json()
    return {muscle["name"]: muscle["id"] for muscle in muscles}
