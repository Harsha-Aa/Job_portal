import streamlit as st
from typing import List, Dict, Optional
import uuid
from datetime import datetime

class DataStore:
    """
    Simple in-memory data store for job portal data
    Uses Streamlit session state for persistence
    """
    
    def __init__(self):
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage containers in session state"""
        if 'jobs_data' not in st.session_state:
            st.session_state.jobs_data = []
        
        if 'applications_data' not in st.session_state:
            st.session_state.applications_data = []
        
        if 'users_data' not in st.session_state:
            st.session_state.users_data = []
    
    # Job-related methods
    def add_job(self, job_data: Dict) -> str:
        """
        Add a new job posting
        
        Args:
            job_data: Job information dictionary
            
        Returns:
            str: Job ID
        """
        if 'id' not in job_data:
            job_data['id'] = str(uuid.uuid4())
        
        job_data['created_at'] = datetime.now().isoformat()
        job_data['updated_at'] = datetime.now().isoformat()
        
        st.session_state.jobs_data.append(job_data)
        return job_data['id']
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """
        Get a specific job by ID
        
        Args:
            job_id: Job ID
            
        Returns:
            Dict: Job data or None if not found
        """
        for job in st.session_state.jobs_data:
            if job.get('id') == job_id:
                return job
        return None
    
    def get_all_jobs(self) -> List[Dict]:
        """
        Get all job postings
        
        Returns:
            List[Dict]: List of all jobs
        """
        return st.session_state.jobs_data.copy()
    
    def update_job(self, job_id: str, updates: Dict) -> bool:
        """
        Update a job posting
        
        Args:
            job_id: Job ID
            updates: Dictionary of updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        for i, job in enumerate(st.session_state.jobs_data):
            if job.get('id') == job_id:
                st.session_state.jobs_data[i].update(updates)
                st.session_state.jobs_data[i]['updated_at'] = datetime.now().isoformat()
                return True
        return False
    
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
        for i, job in enumerate(st.session_state.jobs_data):
            if job.get('id') == job_id:
                del st.session_state.jobs_data[i]
                return True
        return False
    
    def search_jobs(self, query: str, filters: Dict = None) -> List[Dict]:
        """
        Search jobs with query and filters
        
        Args:
            query: Search query
            filters: Filter criteria
            
        Returns:
            List[Dict]: Matching jobs
        """
        results = []
        query_lower = query.lower() if query else ""
        
        for job in st.session_state.jobs_data:
            # Text search
            if query_lower:
                searchable_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('company', '')} {job.get('required_skills', '')}".lower()
                if query_lower not in searchable_text:
                    continue
            
            # Apply filters
            if filters:
                match = True
                for key, value in filters.items():
                    if key in job and job[key] != value:
                        match = False
                        break
                if not match:
                    continue
            
            results.append(job)
        
        return results
    
    def get_jobs_by_company(self, company: str) -> List[Dict]:
        """
        Get jobs by company
        
        Args:
            company: Company name
            
        Returns:
            List[Dict]: Jobs from the company
        """
        return [job for job in st.session_state.jobs_data if job.get('company') == company]
    
    def get_active_jobs(self) -> List[Dict]:
        """
        Get all active jobs
        
        Returns:
            List[Dict]: Active jobs
        """
        return [job for job in st.session_state.jobs_data if job.get('status') == 'active']
    
    # Application-related methods
    def add_application(self, application_data: Dict) -> str:
        """
        Add a new job application
        
        Args:
            application_data: Application information
            
        Returns:
            str: Application ID
        """
        if 'id' not in application_data:
            application_data['id'] = str(uuid.uuid4())
        
        application_data['created_at'] = datetime.now().isoformat()
        application_data['updated_at'] = datetime.now().isoformat()
        
        st.session_state.applications_data.append(application_data)
        return application_data['id']
    
    def get_application(self, application_id: str) -> Optional[Dict]:
        """
        Get a specific application by ID
        
        Args:
            application_id: Application ID
            
        Returns:
            Dict: Application data or None if not found
        """
        for app in st.session_state.applications_data:
            if app.get('id') == application_id:
                return app
        return None
    
    def get_all_applications(self) -> List[Dict]:
        """
        Get all applications
        
        Returns:
            List[Dict]: List of all applications
        """
        return st.session_state.applications_data.copy()
    
    def get_applications_for_job(self, job_id: str) -> List[Dict]:
        """
        Get applications for a specific job
        
        Args:
            job_id: Job ID
            
        Returns:
            List[Dict]: Applications for the job
        """
        return [app for app in st.session_state.applications_data if app.get('job_id') == job_id]
    
    def get_applications_by_email(self, email: str) -> List[Dict]:
        """
        Get applications by applicant email
        
        Args:
            email: Applicant email
            
        Returns:
            List[Dict]: Applications by the applicant
        """
        return [app for app in st.session_state.applications_data if app.get('applicant_email') == email]
    
    def update_application(self, application_id: str, updates: Dict) -> bool:
        """
        Update an application
        
        Args:
            application_id: Application ID
            updates: Dictionary of updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        for i, app in enumerate(st.session_state.applications_data):
            if app.get('id') == application_id:
                st.session_state.applications_data[i].update(updates)
                st.session_state.applications_data[i]['updated_at'] = datetime.now().isoformat()
                return True
        return False
    
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
        for i, app in enumerate(st.session_state.applications_data):
            if app.get('id') == application_id:
                del st.session_state.applications_data[i]
                return True
        return False
    
    # Analytics methods
    def get_job_statistics(self) -> Dict:
        """
        Get job statistics
        
        Returns:
            Dict: Job statistics
        """
        jobs = st.session_state.jobs_data
        
        stats = {
            'total_jobs': len(jobs),
            'active_jobs': len([j for j in jobs if j.get('status') == 'active']),
            'inactive_jobs': len([j for j in jobs if j.get('status') == 'inactive']),
            'companies': len(set(j.get('company', '') for j in jobs)),
            'locations': len(set(j.get('location', '') for j in jobs)),
            'employment_types': {}
        }
        
        # Count employment types
        for job in jobs:
            emp_type = job.get('employment_type', 'Unknown')
            stats['employment_types'][emp_type] = stats['employment_types'].get(emp_type, 0) + 1
        
        return stats
    
    def get_application_statistics(self) -> Dict:
        """
        Get application statistics
        
        Returns:
            Dict: Application statistics
        """
        apps = st.session_state.applications_data
        
        stats = {
            'total_applications': len(apps),
            'unique_applicants': len(set(a.get('applicant_email', '') for a in apps)),
            'status_breakdown': {},
            'average_match_score': 0
        }
        
        # Count statuses
        for app in apps:
            status = app.get('status', 'Unknown')
            stats['status_breakdown'][status] = stats['status_breakdown'].get(status, 0) + 1
        
        # Calculate average match score
        scores = [app.get('match_score', 0) for app in apps if app.get('match_score', 0) > 0]
        if scores:
            stats['average_match_score'] = sum(scores) / len(scores)
        
        return stats
    
    # Data management methods
    def clear_all_jobs(self):
        """Clear all job data"""
        st.session_state.jobs_data = []
    
    def clear_all_applications(self):
        """Clear all application data"""
        st.session_state.applications_data = []
    
    def clear_all_data(self):
        """Clear all data"""
        st.session_state.jobs_data = []
        st.session_state.applications_data = []
        st.session_state.users_data = []
    
    def export_jobs_data(self) -> List[Dict]:
        """
        Export jobs data for backup
        
        Returns:
            List[Dict]: All jobs data
        """
        return st.session_state.jobs_data.copy()
    
    def export_applications_data(self) -> List[Dict]:
        """
        Export applications data for backup
        
        Returns:
            List[Dict]: All applications data
        """
        return st.session_state.applications_data.copy()
    
    def import_jobs_data(self, jobs_data: List[Dict]):
        """
        Import jobs data from backup
        
        Args:
            jobs_data: List of job dictionaries
        """
        st.session_state.jobs_data = jobs_data
    
    def import_applications_data(self, applications_data: List[Dict]):
        """
        Import applications data from backup
        
        Args:
            applications_data: List of application dictionaries
        """
        st.session_state.applications_data = applications_data
