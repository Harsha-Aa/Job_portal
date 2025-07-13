import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.data_store import DataStore

# Initialize data store
if 'data_store' not in st.session_state:
    st.session_state.data_store = DataStore()

st.set_page_config(page_title="Admin Dashboard - AI Job Portal", page_icon="⚙️", layout="wide")

st.title("⚙️ Admin Dashboard")
st.markdown("Comprehensive overview of job portal analytics and management")

# Get data
data_store = st.session_state.data_store
jobs = data_store.get_all_jobs()
applications = data_store.get_all_applications()

# Sidebar for admin authentication (simple password check)
st.sidebar.header("Admin Access")
admin_password = st.sidebar.text_input("Enter Admin Password", type="password")

if admin_password != "admin123":
    st.warning("⚠️ Please enter the admin password to access this dashboard")
    st.stop()

# Main dashboard content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "💼 Jobs Management", "📄 Applications", "⚙️ Settings"])

with tab1:
    st.header("📊 Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", len(jobs), 
                 delta=len([j for j in jobs if j.get('posted_date', '').startswith(datetime.now().strftime("%Y-%m-%d"))]))
    
    with col2:
        st.metric("Active Jobs", len([j for j in jobs if j.get('status') == 'active']))
    
    with col3:
        st.metric("Total Applications", len(applications))
    
    with col4:
        avg_match_score = sum(app.get('match_score', 0) for app in applications) / len(applications) if applications else 0
        st.metric("Avg Match Score", f"{avg_match_score:.1f}%")
    
    # Charts
    if jobs and applications:
        col1, col2 = st.columns(2)
        
        with col1:
            # Jobs by company
            company_counts = {}
            for job in jobs:
                company = job.get('company', 'Unknown')
                company_counts[company] = company_counts.get(company, 0) + 1
            
            if company_counts:
                fig_companies = px.bar(
                    x=list(company_counts.values()),
                    y=list(company_counts.keys()),
                    orientation='h',
                    title="Jobs by Company",
                    labels={'x': 'Number of Jobs', 'y': 'Company'}
                )
                st.plotly_chart(fig_companies, use_container_width=True)
        
        with col2:
            # Applications by job
            job_app_counts = {}
            for app in applications:
                job_title = app.get('job_title', 'Unknown')
                job_app_counts[job_title] = job_app_counts.get(job_title, 0) + 1
            
            if job_app_counts:
                fig_apps = px.pie(
                    values=list(job_app_counts.values()),
                    names=list(job_app_counts.keys()),
                    title="Applications by Job"
                )
                st.plotly_chart(fig_apps, use_container_width=True)
        
        # Application trends
        if applications:
            # Parse dates and create timeline
            app_dates = []
            for app in applications:
                try:
                    date_str = app.get('application_date', '')
                    if date_str:
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        app_dates.append(date.date())
                except:
                    continue
            
            if app_dates:
                date_counts = {}
                for date in app_dates:
                    date_counts[date] = date_counts.get(date, 0) + 1
                
                df_timeline = pd.DataFrame(list(date_counts.items()), columns=['Date', 'Applications'])
                df_timeline = df_timeline.sort_values('Date')
                
                fig_timeline = px.line(
                    df_timeline, 
                    x='Date', 
                    y='Applications',
                    title="Application Trends Over Time"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Match score distribution
        if applications:
            match_scores = [app.get('match_score', 0) for app in applications if app.get('match_score', 0) > 0]
            
            if match_scores:
                fig_scores = px.histogram(
                    x=match_scores,
                    nbins=10,
                    title="Match Score Distribution",
                    labels={'x': 'Match Score (%)', 'y': 'Number of Applications'}
                )
                st.plotly_chart(fig_scores, use_container_width=True)

with tab2:
    st.header("💼 Jobs Management")
    
    if jobs:
        # Job statistics
        active_jobs = [j for j in jobs if j.get('status') == 'active']
        inactive_jobs = [j for j in jobs if j.get('status') == 'inactive']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Active Jobs:** {len(active_jobs)}")
        with col2:
            st.warning(f"**Inactive Jobs:** {len(inactive_jobs)}")
        with col3:
            st.success(f"**Total Jobs:** {len(jobs)}")
        
        # Jobs table
        st.subheader("All Jobs")
        
        # Convert to DataFrame for better display
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'ID': job.get('id', '')[:8] + '...',
                'Title': job.get('title', 'N/A'),
                'Company': job.get('company', 'N/A'),
                'Location': job.get('location', 'N/A'),
                'Status': job.get('status', 'N/A'),
                'Posted Date': job.get('posted_date', 'N/A'),
                'Applications': len(data_store.get_applications_for_job(job.get('id')))
            })
        
        df_jobs = pd.DataFrame(jobs_data)
        st.dataframe(df_jobs, use_container_width=True)
        
        # Bulk actions
        st.subheader("Bulk Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Activate All Jobs", use_container_width=True):
                for job in jobs:
                    data_store.update_job_status(job.get('id'), 'active')
                st.success("All jobs activated!")
                st.rerun()
        
        with col2:
            if st.button("⏸️ Deactivate All Jobs", use_container_width=True):
                for job in jobs:
                    data_store.update_job_status(job.get('id'), 'inactive')
                st.success("All jobs deactivated!")
                st.rerun()

with tab3:
    st.header("📄 Applications Management")
    
    if applications:
        # Application statistics
        submitted_apps = [a for a in applications if a.get('status') == 'submitted']
        under_review_apps = [a for a in applications if a.get('status') == 'under_review']
        accepted_apps = [a for a in applications if a.get('status') == 'accepted']
        rejected_apps = [a for a in applications if a.get('status') == 'rejected']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"**Submitted:** {len(submitted_apps)}")
        with col2:
            st.warning(f"**Under Review:** {len(under_review_apps)}")
        with col3:
            st.success(f"**Accepted:** {len(accepted_apps)}")
        with col4:
            st.error(f"**Rejected:** {len(rejected_apps)}")
        
        # Applications table
        st.subheader("All Applications")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Filter by Status", 
                                       ["All", "submitted", "under_review", "accepted", "rejected"])
        
        with col2:
            job_filter = st.selectbox("Filter by Job", 
                                    ["All"] + list(set(app.get('job_title', '') for app in applications)))
        
        with col3:
            min_score = st.slider("Minimum Match Score", 0, 100, 0)
        
        # Apply filters
        filtered_apps = applications.copy()
        
        if status_filter != "All":
            filtered_apps = [app for app in filtered_apps if app.get('status') == status_filter]
        
        if job_filter != "All":
            filtered_apps = [app for app in filtered_apps if app.get('job_title') == job_filter]
        
        filtered_apps = [app for app in filtered_apps if app.get('match_score', 0) >= min_score]
        
        st.markdown(f"**Showing {len(filtered_apps)} applications**")
        
        # Display applications
        for app in filtered_apps:
            with st.expander(f"📄 {app.get('applicant_name')} - {app.get('job_title')} ({app.get('match_score', 0):.1f}% match)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Applicant:** {app.get('applicant_name')}")
                    st.write(f"**Email:** {app.get('applicant_email')}")
                    st.write(f"**Phone:** {app.get('applicant_phone', 'N/A')}")
                    st.write(f"**Job:** {app.get('job_title')} at {app.get('company')}")
                    st.write(f"**Applied:** {app.get('application_date')}")
                    st.write(f"**Current Status:** {app.get('status')}")
                    
                    if app.get('cover_letter'):
                        with st.expander("Cover Letter"):
                            st.write(app.get('cover_letter'))
                    
                    with st.expander("Resume Preview"):
                        resume_text = app.get('resume_text', '')
                        st.text_area("Resume Content", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text, 
                                   height=150, disabled=True)
                
                with col2:
                    st.metric("Match Score", f"{app.get('match_score', 0):.1f}%")
                    
                    # Status update
                    new_status = st.selectbox("Update Status", 
                                            ["submitted", "under_review", "accepted", "rejected"],
                                            index=["submitted", "under_review", "accepted", "rejected"].index(app.get('status', 'submitted')),
                                            key=f"status_{app.get('id')}")
                    
                    if st.button("Update Status", key=f"update_{app.get('id')}"):
                        data_store.update_application_status(app.get('id'), new_status)
                        st.success(f"Status updated to {new_status}")
                        st.rerun()
    else:
        st.info("No applications submitted yet.")

with tab4:
    st.header("⚙️ System Settings")
    
    # Data management
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Data**")
        
        if st.button("📥 Export Jobs as CSV", use_container_width=True):
            if jobs:
                df_jobs = pd.DataFrame(jobs)
                csv = df_jobs.to_csv(index=False)
                st.download_button(
                    label="Download Jobs CSV",
                    data=csv,
                    file_name=f"jobs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        if st.button("📥 Export Applications as CSV", use_container_width=True):
            if applications:
                # Remove resume_text for CSV export (too large)
                apps_for_export = []
                for app in applications:
                    app_copy = app.copy()
                    app_copy.pop('resume_text', None)
                    apps_for_export.append(app_copy)
                
                df_apps = pd.DataFrame(apps_for_export)
                csv = df_apps.to_csv(index=False)
                st.download_button(
                    label="Download Applications CSV",
                    data=csv,
                    file_name=f"applications_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with col2:
        st.write("**Clear Data**")
        
        if st.button("🗑️ Clear All Jobs", use_container_width=True):
            if st.button("⚠️ Confirm Delete All Jobs", use_container_width=True):
                data_store.clear_all_jobs()
                st.success("All jobs cleared!")
                st.rerun()
        
        if st.button("🗑️ Clear All Applications", use_container_width=True):
            if st.button("⚠️ Confirm Delete All Applications", use_container_width=True):
                data_store.clear_all_applications()
                st.success("All applications cleared!")
                st.rerun()
    
    # System information
    st.subheader("System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Total Jobs:** {len(jobs)}")
        st.info(f"**Total Applications:** {len(applications)}")
        st.info(f"**Active Jobs:** {len([j for j in jobs if j.get('status') == 'active'])}")
    
    with col2:
        st.info(f"**Companies:** {len(set(job.get('company', '') for job in jobs))}")
        st.info(f"**Unique Applicants:** {len(set(app.get('applicant_email', '') for app in applications))}")
        st.info(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
    if st.button("🔍 Browse Jobs", use_container_width=True):
        st.switch_page("pages/2_Apply_for_Jobs.py")
