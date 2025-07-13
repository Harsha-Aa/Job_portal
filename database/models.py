"""
Database models for the job portal application
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default='seeker')  # seeker, employer, admin
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    jobs = relationship("Job", back_populates="employer", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="applicant", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check if password matches"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'phone': self.phone,
            'company': self.company,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    employment_type = Column(String(50), nullable=False)  # full-time, part-time, contract, internship
    salary = Column(String(100), nullable=True)
    experience_level = Column(String(50), nullable=False)
    remote_option = Column(String(50), nullable=False)  # on-site, remote, hybrid
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=True)
    additional_requirements = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=False)
    status = Column(String(50), default='active')  # active, inactive, closed
    employer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employer = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'employment_type': self.employment_type,
            'salary': self.salary,
            'experience_level': self.experience_level,
            'remote_option': self.remote_option,
            'description': self.description,
            'required_skills': self.required_skills,
            'additional_requirements': self.additional_requirements,
            'contact_email': self.contact_email,
            'status': self.status,
            'employer_id': self.employer_id,
            'posted_date': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    applicant_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resume_text = Column(Text, nullable=False)
    cover_letter = Column(Text, nullable=True)
    match_score = Column(Float, default=0.0)
    status = Column(String(50), default='submitted')  # submitted, under_review, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
    
    def to_dict(self):
        """Convert application to dictionary"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'company': self.job.company if self.job else None,
            'applicant_id': self.applicant_id,
            'applicant_name': f"{self.applicant.first_name} {self.applicant.last_name}" if self.applicant else None,
            'applicant_email': self.applicant.email if self.applicant else None,
            'applicant_phone': self.applicant.phone if self.applicant else None,
            'resume_text': self.resume_text,
            'cover_letter': self.cover_letter,
            'match_score': self.match_score,
            'status': self.status,
            'application_date': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }