import streamlit as st
from datetime import datetime
import uuid
from utils.data_store import DataStore

# Initialize data store
if 'data_store' not in st.session_state:
    st.session_state.data_store = DataStore()

st.set_page_config(page_title="Job Postings - AI Job Portal", page_icon="📝", layout="wide")

st.title("📝 Job Postings")
st.markdown("Post new job opportunities and manage existing listings")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["➕ Post New Job", "📋 Manage Jobs"])

with tab1:
    st.header("Create New Job Posting")
    
    with st.form("job_posting_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name *", placeholder="e.g., Tech Corp")
            job_title = st.text_input("Job Title *", placeholder="e.g., Senior Software Engineer")
            location = st.text_input("Location *", placeholder="e.g., New York, NY")
            employment_type = st.selectbox("Employment Type", 
                                         ["Full-time", "Part-time", "Contract", "Internship"])
            
        with col2:
            salary_range = st.text_input("Salary Range", placeholder="e.g., $70,000 - $90,000")
            experience_level = st.selectbox("Experience Level", 
                                          ["Entry Level", "Mid Level", "Senior Level", "Executive"])
            remote_option = st.selectbox("Remote Work", 
                                       ["On-site", "Remote", "Hybrid"])
            contact_email = st.text_input("Contact Email *", placeholder="hr@company.com")
        
        # Job description
        job_description = st.text_area("Job Description *", 
                                     placeholder="Describe the role, responsibilities, and requirements...", 
                                     height=150)
        
        # Required skills
        required_skills = st.text_area("Required Skills", 
                                     placeholder="e.g., Python, React, SQL, Machine Learning", 
                                     height=100)
        
        # Additional requirements
        additional_requirements = st.text_area("Additional Requirements", 
                                             placeholder="Education, certifications, etc.", 
                                             height=100)
        
        submitted = st.form_submit_button("🚀 Post Job", use_container_width=True)
        
        if submitted:
            if company_name and job_title and location and job_description and contact_email:
                # Create job posting
                job_data = {
                    'id': str(uuid.uuid4()),
                    'company': company_name,
                    'title': job_title,
                    'location': location,
                    'employment_type': employment_type,
                    'salary': salary_range,
                    'experience_level': experience_level,
                    'remote_option': remote_option,
                    'contact_email': contact_email,
                    'description': job_description,
                    'required_skills': required_skills,
                    'additional_requirements': additional_requirements,
                    'posted_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'active'
                }
                
                # Save to data store
                st.session_state.data_store.add_job(job_data)
                st.success("✅ Job posted successfully!")
                st.balloons()
                
                # Show preview
                st.markdown("### Job Preview:")
                st.info(f"**{job_title}** at **{company_name}**\n\n"
                       f"📍 {location} • 💼 {employment_type} • 🏠 {remote_option}\n\n"
                       f"💰 {salary_range}\n\n"
                       f"**Description:** {job_description[:200]}...")
                
            else:
                st.error("⚠️ Please fill in all required fields marked with *")

with tab2:
    st.header("Manage Job Postings")
    
    jobs = st.session_state.data_store.get_all_jobs()
    
    if jobs:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_company = st.selectbox("Filter by Company", 
                                        ["All"] + list(set(job.get('company', '') for job in jobs)))
        
        with col2:
            filter_status = st.selectbox("Filter by Status", 
                                       ["All", "active", "inactive"])
        
        with col3:
            search_term = st.text_input("Search Jobs", placeholder="Search by title or description...")
        
        # Apply filters
        filtered_jobs = jobs.copy()
        
        if filter_company != "All":
            filtered_jobs = [job for job in filtered_jobs if job.get('company') == filter_company]
        
        if filter_status != "All":
            filtered_jobs = [job for job in filtered_jobs if job.get('status') == filter_status]
        
        if search_term:
            filtered_jobs = [job for job in filtered_jobs 
                           if search_term.lower() in job.get('title', '').lower() 
                           or search_term.lower() in job.get('description', '').lower()]
        
        st.markdown(f"**Found {len(filtered_jobs)} jobs**")
        
        # Display jobs
        for job in filtered_jobs:
            with st.expander(f"💼 {job.get('title', 'N/A')} - {job.get('company', 'N/A')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Location:** {job.get('location', 'N/A')}")
                    st.write(f"**Employment Type:** {job.get('employment_type', 'N/A')}")
                    st.write(f"**Salary:** {job.get('salary', 'N/A')}")
                    st.write(f"**Posted:** {job.get('posted_date', 'N/A')}")
                    st.write(f"**Status:** {job.get('status', 'N/A')}")
                    st.write(f"**Contact:** {job.get('contact_email', 'N/A')}")
                    
                    with st.expander("Job Description"):
                        st.write(job.get('description', 'N/A'))
                    
                    if job.get('required_skills'):
                        st.write(f"**Required Skills:** {job.get('required_skills')}")
                
                with col2:
                    # Job actions
                    if job.get('status') == 'active':
                        if st.button("⏸️ Deactivate", key=f"deactivate_{job.get('id')}"):
                            st.session_state.data_store.update_job_status(job.get('id'), 'inactive')
                            st.success("Job deactivated!")
                            st.rerun()
                    else:
                        if st.button("▶️ Activate", key=f"activate_{job.get('id')}"):
                            st.session_state.data_store.update_job_status(job.get('id'), 'active')
                            st.success("Job activated!")
                            st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"delete_{job.get('id')}"):
                        st.session_state.data_store.delete_job(job.get('id'))
                        st.success("Job deleted!")
                        st.rerun()
                    
                    # View applications
                    applications = st.session_state.data_store.get_applications_for_job(job.get('id'))
                    st.metric("Applications", len(applications))
    else:
        st.info("No jobs posted yet. Use the form above to post your first job!")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🔍 Browse Jobs", use_container_width=True):
        st.switch_page("pages/2_Apply_for_Jobs.py")

with col3:
    if st.button("⚙️ Admin Dashboard", use_container_width=True):
        st.switch_page("pages/3_Admin_Dashboard.py")
