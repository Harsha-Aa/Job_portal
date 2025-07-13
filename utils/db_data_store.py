"""
Database-backed data store for job portal
Replaces the session-based storage with SQLite persistence
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from database.database import SessionLocal, engine
from database.models import User, Job, Application
from datetime import datetime

class DatabaseDataStore:
    """
    Database-backed data store using SQLAlchemy
    Replaces the session state storage
    """
    
    def __init__(self):
        self.Session = SessionLocal
    
    def get_db_session(self):
        """Get database session"""
        return self.Session()
    
    # Job-related methods
    def add_job(self, job_data: Dict, employer_id: int) -> str:
        """
        Add a new job posting
        
        Args:
            job_data: Job information dictionary
            employer_id: ID of the employer creating the job
            
        Returns:
            str: Job ID
        """
        db = self.get_db_session()
        try:
            job = Job(
                title=job_data.get('title'),
                company=job_data.get('company'),
                location=job_data.get('location'),
                employment_type=job_data.get('employment_type'),
                salary=job_data.get('salary'),
                experience_level=job_data.get('experience_level'),
                remote_option=job_data.get('remote_option'),
                description=job_data.get('description'),
                required_skills=job_data.get('required_skills'),
                additional_requirements=job_data.get('additional_requirements'),
                contact_email=job_data.get('contact_email'),
                status=job_data.get('status', 'active'),
                employer_id=employer_id
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            return str(job.id)
        finally:
            db.close()
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """
        Get a specific job by ID
        
        Args:
            job_id: Job ID
            
        Returns:
            Dict: Job data or None if not found
        """
        db = self.get_db_session()
        try:
            job = db.query(Job).filter(Job.id == int(job_id)).first()
            return job.to_dict() if job else None
        finally:
            db.close()
    
    def get_all_jobs(self) -> List[Dict]:
        """
        Get all job postings
        
        Returns:
            List[Dict]: List of all jobs
        """
        db = self.get_db_session()
        try:
            jobs = db.query(Job).all()
            return [job.to_dict() for job in jobs]
        finally:
            db.close()
    
    def update_job(self, job_id: str, updates: Dict) -> bool:
        """
        Update a job posting
        
        Args:
            job_id: Job ID
            updates: Dictionary of updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        db = self.get_db_session()
        try:
            job = db.query(Job).filter(Job.id == int(job_id)).first()
            if job:
                for key, value in updates.items():
                    setattr(job, key, value)
                job.updated_at = datetime.utcnow()
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def update_job_status(self, job_id: str, status: str) -> bool:
        """
        Update job status
        
        Args:
            job_id: Job ID
            status: New status
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.update_job(job_id, {'status': status})
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job posting
        
        Args:
            job_id: Job ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        db = self.get_db_session()
        try:
            job = db.query(Job).filter(Job.id == int(job_id)).first()
            if job:
                db.delete(job)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def search_jobs(self, query: str, filters: Dict = None) -> List[Dict]:
        """
        Search jobs with query and filters
        
        Args:
            query: Search query
            filters: Filter criteria
            
        Returns:
            List[Dict]: Matching jobs
        """
        db = self.get_db_session()
        try:
            jobs_query = db.query(Job)
            
            # Apply text search
            if query:
                search_filter = or_(
                    Job.title.ilike(f'%{query}%'),
                    Job.description.ilike(f'%{query}%'),
                    Job.company.ilike(f'%{query}%'),
                    Job.required_skills.ilike(f'%{query}%')
                )
                jobs_query = jobs_query.filter(search_filter)
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(Job, key) and value:
                        jobs_query = jobs_query.filter(getattr(Job, key) == value)
            
            jobs = jobs_query.all()
            return [job.to_dict() for job in jobs]
        finally:
            db.close()
    
    def get_jobs_by_company(self, company: str) -> List[Dict]:
        """
        Get jobs by company
        
        Args:
            company: Company name
            
        Returns:
            List[Dict]: Jobs from the company
        """
        db = self.get_db_session()
        try:
            jobs = db.query(Job).filter(Job.company == company).all()
            return [job.to_dict() for job in jobs]
        finally:
            db.close()
    
    def get_active_jobs(self) -> List[Dict]:
        """
        Get all active jobs
        
        Returns:
            List[Dict]: Active jobs
        """
        db = self.get_db_session()
        try:
            jobs = db.query(Job).filter(Job.status == 'active').all()
            return [job.to_dict() for job in jobs]
        finally:
            db.close()
    
    def get_jobs_by_employer(self, employer_id: int) -> List[Dict]:
        """
        Get jobs by employer ID
        
        Args:
            employer_id: Employer user ID
            
        Returns:
            List[Dict]: Jobs by the employer
        """
        db = self.get_db_session()
        try:
            jobs = db.query(Job).filter(Job.employer_id == employer_id).all()
            return [job.to_dict() for job in jobs]
        finally:
            db.close()
    
    # Application-related methods
    def add_application(self, application_data: Dict) -> str:
        """
        Add a new job application
        
        Args:
            application_data: Application information
            
        Returns:
            str: Application ID
        """
        db = self.get_db_session()
        try:
            application = Application(
                job_id=application_data.get('job_id'),
                applicant_id=application_data.get('applicant_id'),
                resume_text=application_data.get('resume_text'),
                cover_letter=application_data.get('cover_letter'),
                match_score=application_data.get('match_score', 0.0),
                status=application_data.get('status', 'submitted')
            )
            db.add(application)
            db.commit()
            db.refresh(application)
            return str(application.id)
        finally:
            db.close()
    
    def get_application(self, application_id: str) -> Optional[Dict]:
        """
        Get a specific application by ID
        
        Args:
            application_id: Application ID
            
        Returns:
            Dict: Application data or None if not found
        """
        db = self.get_db_session()
        try:
            application = db.query(Application).filter(Application.id == int(application_id)).first()
            return application.to_dict() if application else None
        finally:
            db.close()
    
    def get_all_applications(self) -> List[Dict]:
        """
        Get all applications
        
        Returns:
            List[Dict]: List of all applications
        """
        db = self.get_db_session()
        try:
            applications = db.query(Application).all()
            return [app.to_dict() for app in applications]
        finally:
            db.close()
    
    def get_applications_for_job(self, job_id: str) -> List[Dict]:
        """
        Get applications for a specific job
        
        Args:
            job_id: Job ID
            
        Returns:
            List[Dict]: Applications for the job
        """
        db = self.get_db_session()
        try:
            applications = db.query(Application).filter(Application.job_id == int(job_id)).all()
            return [app.to_dict() for app in applications]
        finally:
            db.close()
    
    def get_applications_by_email(self, email: str) -> List[Dict]:
        """
        Get applications by applicant email
        
        Args:
            email: Applicant email
            
        Returns:
            List[Dict]: Applications by the applicant
        """
        db = self.get_db_session()
        try:
            applications = db.query(Application).join(User).filter(User.email == email).all()
            return [app.to_dict() for app in applications]
        finally:
            db.close()
    
    def get_applications_by_user(self, user_id: int) -> List[Dict]:
        """
        Get applications by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            List[Dict]: Applications by the user
        """
        db = self.get_db_session()
        try:
            applications = db.query(Application).filter(Application.applicant_id == user_id).all()
            return [app.to_dict() for app in applications]
        finally:
            db.close()
    
    def update_application(self, application_id: str, updates: Dict) -> bool:
        """
        Update an application
        
        Args:
            application_id: Application ID
            updates: Dictionary of updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        db = self.get_db_session()
        try:
            application = db.query(Application).filter(Application.id == int(application_id)).first()
            if application:
                for key, value in updates.items():
                    setattr(application, key, value)
                application.updated_at = datetime.utcnow()
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def update_application_status(self, application_id: str, status: str) -> bool:
        """
        Update application status
        
        Args:
            application_id: Application ID
            status: New status
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.update_application(application_id, {'status': status})
    
    def delete_application(self, application_id: str) -> bool:
        """
        Delete an application
        
        Args:
            application_id: Application ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        db = self.get_db_session()
        try:
            application = db.query(Application).filter(Application.id == int(application_id)).first()
            if application:
                db.delete(application)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    # Statistics and analytics
    def get_job_statistics(self) -> Dict:
        """
        Get job statistics
        
        Returns:
            Dict: Job statistics
        """
        db = self.get_db_session()
        try:
            total_jobs = db.query(Job).count()
            active_jobs = db.query(Job).filter(Job.status == 'active').count()
            inactive_jobs = db.query(Job).filter(Job.status == 'inactive').count()
            
            companies = db.query(Job.company).distinct().count()
            locations = db.query(Job.location).distinct().count()
            
            return {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'inactive_jobs': inactive_jobs,
                'companies': companies,
                'locations': locations
            }
        finally:
            db.close()
    
    def get_application_statistics(self) -> Dict:
        """
        Get application statistics
        
        Returns:
            Dict: Application statistics
        """
        db = self.get_db_session()
        try:
            total_applications = db.query(Application).count()
            unique_applicants = db.query(Application.applicant_id).distinct().count()
            
            # Calculate average match score
            applications = db.query(Application).all()
            scores = [app.match_score for app in applications if app.match_score > 0]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            return {
                'total_applications': total_applications,
                'unique_applicants': unique_applicants,
                'average_match_score': avg_score
            }
        finally:
            db.close()
    
    # Data management
    def clear_all_jobs(self):
        """Clear all job data"""
        db = self.get_db_session()
        try:
            db.query(Job).delete()
            db.commit()
        finally:
            db.close()
    
    def clear_all_applications(self):
        """Clear all application data"""
        db = self.get_db_session()
        try:
            db.query(Application).delete()
            db.commit()
        finally:
            db.close()
    
    def export_jobs_data(self) -> List[Dict]:
        """
        Export jobs data for backup
        
        Returns:
            List[Dict]: All jobs data
        """
        return self.get_all_jobs()
    
    def export_applications_data(self) -> List[Dict]:
        """
        Export applications data for backup
        
        Returns:
            List[Dict]: All applications data
        """
        return self.get_all_applications()