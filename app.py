import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db_data_store import DatabaseDataStore
from utils.auth import AuthManager, show_login_form
from database.database import init_database

# Initialize database
init_database()

# Initialize data store and auth
if 'data_store' not in st.session_state:
    st.session_state.data_store = DatabaseDataStore()

auth = AuthManager()

# Page configuration
st.set_page_config(
    page_title="AI-Powered Job Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bootstrap-like styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        text-align: center;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI-Powered Job Portal</h1>
    <p style="text-align: center; color: white; margin: 0;">Find the perfect job match with ML-powered resume analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation and authentication
st.sidebar.title("Navigation")
show_login_form()
st.sidebar.markdown("---")

# Display statistics
data_store = st.session_state.data_store
total_jobs = len(data_store.get_all_jobs())
total_applications = len(data_store.get_all_applications())
total_companies = len(set(job.get('company', '') for job in data_store.get_all_jobs()))

# Statistics cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #667eea; margin: 0;">📊 Total Jobs</h3>
        <h2 style="margin: 0.5rem 0 0 0;">{total_jobs}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #667eea; margin: 0;">👥 Applications</h3>
        <h2 style="margin: 0.5rem 0 0 0;">{total_applications}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #667eea; margin: 0;">🏢 Companies</h3>
        <h2 style="margin: 0.5rem 0 0 0;">{total_companies}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Recent jobs section
st.markdown("## 🎯 Recent Job Postings")

jobs = data_store.get_all_jobs()
if jobs:
    # Display recent jobs (last 5)
    recent_jobs = sorted(jobs, key=lambda x: x.get('posted_date', ''), reverse=True)[:5]
    
    for job in recent_jobs:
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h4 style="color: #28a745; margin: 0 0 0.5rem 0;">💼 {job.get('title', 'N/A')}</h4>
                <p style="margin: 0.25rem 0;"><strong>Company:</strong> {job.get('company', 'N/A')}</p>
                <p style="margin: 0.25rem 0;"><strong>Location:</strong> {job.get('location', 'N/A')}</p>
                <p style="margin: 0.25rem 0;"><strong>Salary:</strong> {job.get('salary', 'N/A')}</p>
                <p style="margin: 0.25rem 0;"><strong>Posted:</strong> {job.get('posted_date', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No jobs posted yet. Visit the Job Postings page to add some jobs!")

st.markdown("---")

# Quick actions
st.markdown("## 🚀 Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Post New Job", use_container_width=True):
        st.switch_page("pages/1_Job_Postings.py")

with col2:
    if st.button("🔍 Browse Jobs", use_container_width=True):
        st.switch_page("pages/2_Apply_for_Jobs.py")

with col3:
    if st.button("⚙️ Admin Dashboard", use_container_width=True):
        st.switch_page("pages/3_Admin_Dashboard.py")

# Login prompt for non-authenticated users
if not auth.is_authenticated():
    st.markdown("---")
    st.info("🔐 Please login to access job posting and application features.")
    if st.button("Login / Register", use_container_width=True):
        st.switch_page("pages/login.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Powered by AI • Built with Streamlit • Resume parsing with spaCy</p>
</div>
""", unsafe_allow_html=True)
