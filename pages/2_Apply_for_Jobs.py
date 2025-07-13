import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from utils.data_store import DataStore
from utils.resume_parser import ResumeParser
from utils.job_matcher import JobMatcher

# Initialize components
if 'data_store' not in st.session_state:
    st.session_state.data_store = DataStore()

if 'resume_parser' not in st.session_state:
    st.session_state.resume_parser = ResumeParser()

if 'job_matcher' not in st.session_state:
    st.session_state.job_matcher = JobMatcher()

st.set_page_config(page_title="Apply for Jobs - AI Job Portal", page_icon="🔍", layout="wide")

st.title("🔍 Browse & Apply for Jobs")
st.markdown("Find your perfect job match with AI-powered resume analysis")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["🎯 Find Jobs", "📄 Resume Analysis", "📋 My Applications"])

with tab1:
    st.header("Job Search & Filtering")
    
    jobs = st.session_state.data_store.get_all_jobs()
    active_jobs = [job for job in jobs if job.get('status') == 'active']
    
    if active_jobs:
        # Search and filter section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_query = st.text_input("🔍 Search Jobs", placeholder="Enter keywords...")
            
        with col2:
            location_filter = st.selectbox("📍 Location", 
                                         ["All Locations"] + list(set(job.get('location', '') for job in active_jobs)))
            
        with col3:
            employment_filter = st.selectbox("💼 Employment Type", 
                                           ["All Types"] + list(set(job.get('employment_type', '') for job in active_jobs)))
        
        # Additional filters
        col4, col5 = st.columns(2)
        
        with col4:
            experience_filter = st.selectbox("📊 Experience Level", 
                                           ["All Levels"] + list(set(job.get('experience_level', '') for job in active_jobs)))
        
        with col5:
            remote_filter = st.selectbox("🏠 Remote Work", 
                                       ["All Options"] + list(set(job.get('remote_option', '') for job in active_jobs)))
        
        # Apply filters
        filtered_jobs = active_jobs.copy()
        
        if search_query:
            filtered_jobs = [job for job in filtered_jobs 
                           if search_query.lower() in job.get('title', '').lower() 
                           or search_query.lower() in job.get('description', '').lower()
                           or search_query.lower() in job.get('required_skills', '').lower()]
        
        if location_filter != "All Locations":
            filtered_jobs = [job for job in filtered_jobs if job.get('location') == location_filter]
        
        if employment_filter != "All Types":
            filtered_jobs = [job for job in filtered_jobs if job.get('employment_type') == employment_filter]
        
        if experience_filter != "All Levels":
            filtered_jobs = [job for job in filtered_jobs if job.get('experience_level') == experience_filter]
        
        if remote_filter != "All Options":
            filtered_jobs = [job for job in filtered_jobs if job.get('remote_option') == remote_filter]
        
        st.markdown(f"**Found {len(filtered_jobs)} matching jobs**")
        
        # Display jobs
        for job in filtered_jobs:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### 💼 {job.get('title', 'N/A')}")
                    st.markdown(f"**🏢 {job.get('company', 'N/A')}**")
                    st.markdown(f"📍 {job.get('location', 'N/A')} • 💼 {job.get('employment_type', 'N/A')} • 🏠 {job.get('remote_option', 'N/A')}")
                    
                    if job.get('salary'):
                        st.markdown(f"💰 {job.get('salary')}")
                    
                    st.markdown(f"📊 {job.get('experience_level', 'N/A')}")
                    st.markdown(f"📅 Posted: {job.get('posted_date', 'N/A')}")
                    
                    with st.expander("Job Description"):
                        st.write(job.get('description', 'N/A'))
                        
                        if job.get('required_skills'):
                            st.write(f"**Required Skills:** {job.get('required_skills')}")
                        
                        if job.get('additional_requirements'):
                            st.write(f"**Additional Requirements:** {job.get('additional_requirements')}")
                
                with col2:
                    st.markdown("### Apply Now")
                    
                    with st.form(f"application_form_{job.get('id')}"):
                        applicant_name = st.text_input("Full Name *", key=f"name_{job.get('id')}")
                        applicant_email = st.text_input("Email *", key=f"email_{job.get('id')}")
                        applicant_phone = st.text_input("Phone", key=f"phone_{job.get('id')}")
                        
                        resume_file = st.file_uploader("Upload Resume *", 
                                                     type=['pdf', 'docx'], 
                                                     key=f"resume_{job.get('id')}")
                        
                        cover_letter = st.text_area("Cover Letter", 
                                                  placeholder="Brief introduction...", 
                                                  key=f"cover_{job.get('id')}")
                        
                        submitted = st.form_submit_button("🚀 Apply Now", use_container_width=True)
                        
                        if submitted:
                            if applicant_name and applicant_email and resume_file:
                                # Parse resume
                                resume_text = st.session_state.resume_parser.parse_resume(resume_file)
                                
                                if resume_text:
                                    # Calculate job match score
                                    job_description = f"{job.get('description', '')} {job.get('required_skills', '')}"
                                    match_score = st.session_state.job_matcher.calculate_match_score(
                                        resume_text, job_description
                                    )
                                    
                                    # Create application
                                    application_data = {
                                        'id': str(uuid.uuid4()),
                                        'job_id': job.get('id'),
                                        'job_title': job.get('title'),
                                        'company': job.get('company'),
                                        'applicant_name': applicant_name,
                                        'applicant_email': applicant_email,
                                        'applicant_phone': applicant_phone,
                                        'resume_text': resume_text,
                                        'cover_letter': cover_letter,
                                        'match_score': match_score,
                                        'application_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        'status': 'submitted'
                                    }
                                    
                                    # Save application
                                    st.session_state.data_store.add_application(application_data)
                                    
                                    st.success(f"✅ Application submitted successfully!")
                                    st.info(f"🎯 Job Match Score: {match_score:.1f}%")
                                    
                                    # Show extracted skills
                                    extracted_skills = st.session_state.job_matcher.extract_skills(resume_text)
                                    if extracted_skills:
                                        st.write("**Extracted Skills from Resume:**")
                                        st.write(", ".join(extracted_skills))
                                    
                                else:
                                    st.error("❌ Could not parse resume. Please try a different file.")
                            else:
                                st.error("⚠️ Please fill in all required fields and upload a resume.")
                
                st.markdown("---")
    else:
        st.info("No active jobs available at the moment. Check back later!")

with tab2:
    st.header("Resume Analysis & Optimization")
    
    st.markdown("Upload your resume to get AI-powered insights and optimization suggestions.")
    
    uploaded_file = st.file_uploader("Upload Resume for Analysis", type=['pdf', 'docx'])
    
    if uploaded_file:
        # Parse resume
        resume_text = st.session_state.resume_parser.parse_resume(uploaded_file)
        
        if resume_text:
            st.success("✅ Resume parsed successfully!")
            
            # Show analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Resume Analysis")
                
                # Extract skills
                extracted_skills = st.session_state.job_matcher.extract_skills(resume_text)
                if extracted_skills:
                    st.write("**Extracted Skills:**")
                    st.write(", ".join(extracted_skills))
                
                # Word count
                word_count = len(resume_text.split())
                st.metric("Word Count", word_count)
                
                # Resume score (basic analysis)
                resume_score = min(100, (word_count / 10) + len(extracted_skills) * 5)
                st.metric("Resume Score", f"{resume_score:.1f}/100")
                
                # Show preview
                with st.expander("Resume Text Preview"):
                    st.text_area("Extracted Text", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, 
                               height=200, disabled=True)
            
            with col2:
                st.subheader("🎯 Job Matching Analysis")
                
                # Compare against available jobs
                jobs = st.session_state.data_store.get_all_jobs()
                active_jobs = [job for job in jobs if job.get('status') == 'active']
                
                if active_jobs:
                    job_matches = []
                    
                    for job in active_jobs:
                        job_description = f"{job.get('description', '')} {job.get('required_skills', '')}"
                        match_score = st.session_state.job_matcher.calculate_match_score(
                            resume_text, job_description
                        )
                        job_matches.append({
                            'job': job,
                            'score': match_score
                        })
                    
                    # Sort by match score
                    job_matches.sort(key=lambda x: x['score'], reverse=True)
                    
                    st.write("**Top Job Matches:**")
                    
                    for i, match in enumerate(job_matches[:5]):
                        job = match['job']
                        score = match['score']
                        
                        with st.expander(f"{i+1}. {job.get('title')} - {score:.1f}% match"):
                            st.write(f"**Company:** {job.get('company')}")
                            st.write(f"**Location:** {job.get('location')}")
                            st.write(f"**Match Score:** {score:.1f}%")
                            
                            # Show matching skills
                            job_skills = st.session_state.job_matcher.extract_skills(
                                job.get('required_skills', '')
                            )
                            matching_skills = set(extracted_skills) & set(job_skills)
                            
                            if matching_skills:
                                st.write(f"**Matching Skills:** {', '.join(matching_skills)}")
                else:
                    st.info("No active jobs available for comparison.")
        else:
            st.error("❌ Could not parse resume. Please try a different file.")

with tab3:
    st.header("My Applications")
    
    # Filter applications by email
    applicant_email = st.text_input("Enter your email to view applications", placeholder="your.email@example.com")
    
    if applicant_email:
        applications = st.session_state.data_store.get_applications_by_email(applicant_email)
        
        if applications:
            st.success(f"Found {len(applications)} applications")
            
            # Display applications
            for app in applications:
                with st.expander(f"📄 {app.get('job_title')} at {app.get('company')} - {app.get('status')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Job:** {app.get('job_title')}")
                        st.write(f"**Company:** {app.get('company')}")
                        st.write(f"**Applied:** {app.get('application_date')}")
                        st.write(f"**Status:** {app.get('status')}")
                        
                        if app.get('cover_letter'):
                            st.write(f"**Cover Letter:** {app.get('cover_letter')}")
                    
                    with col2:
                        st.metric("Job Match Score", f"{app.get('match_score', 0):.1f}%")
                        
                        # Show status badge
                        status = app.get('status', 'submitted')
                        if status == 'submitted':
                            st.info("📋 Application Submitted")
                        elif status == 'under_review':
                            st.warning("👀 Under Review")
                        elif status == 'accepted':
                            st.success("✅ Accepted")
                        elif status == 'rejected':
                            st.error("❌ Rejected")
        else:
            st.info("No applications found for this email address.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("📝 Post Jobs", use_container_width=True):
        st.switch_page("pages/1_Job_Postings.py")

with col3:
    if st.button("⚙️ Admin Dashboard", use_container_width=True):
        st.switch_page("pages/3_Admin_Dashboard.py")
