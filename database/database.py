"""
Database configuration and session management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database.models import Base, User, Job, Application

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///job_portal.db")

# Create engine with connection pooling for SQLite
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with tables and default admin user"""
    create_tables()
    
    # Create default admin user if not exists
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == "admin@jobportal.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@jobportal.com",
                first_name="Admin",
                last_name="User",
                role="admin",
                company="Job Portal System"
            )
            admin_user.set_password("admin123")
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin@jobportal.com / admin123")
    finally:
        db.close()

def get_user_by_email(email: str):
    """Get user by email"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def create_user(user_data: dict):
    """Create a new user"""
    db = SessionLocal()
    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()