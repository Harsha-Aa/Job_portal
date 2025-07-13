"""
Login page for the job portal
"""
import streamlit as st
from utils.auth import AuthManager

st.set_page_config(page_title="Login - AI Job Portal", page_icon="🔐", layout="wide")

# Initialize auth manager
auth = AuthManager()

# If already logged in, redirect to main page
if auth.is_authenticated():
    st.switch_page("app.py")

st.title("🔐 Login to Job Portal")

# Create tabs for login and register
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.header("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Home", use_container_width=True):
                st.switch_page("app.py")
        
        if login_button:
            if email and password:
                if auth.login(email, password):
                    st.success("Login successful! Redirecting...")
                    st.switch_page("app.py")
                else:
                    st.error("Invalid email or password. Please try again.")
            else:
                st.error("Please enter both email and password.")

with tab2:
    st.header("Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *")
            last_name = st.text_input("Last Name *")
            email = st.text_input("Email Address *")
            
        with col2:
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            role = st.selectbox("Account Type", ["seeker", "employer"], 
                              help="Seekers apply for jobs, Employers post jobs")
        
        phone = st.text_input("Phone Number (Optional)")
        company = st.text_input("Company Name (Optional)", 
                              help="Required for employer accounts")
        
        register_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if register_button:
            # Validation
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("Please fill in all required fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif role == "employer" and not company:
                st.error("Company name is required for employer accounts.")
            else:
                # Create user
                user_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': password,
                    'role': role,
                    'phone': phone,
                    'company': company if role == "employer" else None
                }
                
                if auth.register_user(user_data):
                    st.success("Account created successfully! Please login.")
                    st.balloons()
                else:
                    st.error("Registration failed. Email may already be in use.")

# Information section
st.markdown("---")
st.markdown("## Demo Accounts")
st.info("""
**Admin Account:**
- Email: admin@jobportal.com
- Password: admin123

**Test the system by creating your own employer or job seeker account!**
""")

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("📝 Job Postings", use_container_width=True):
        st.switch_page("pages/1_Job_Postings.py")

with col3:
    if st.button("🔍 Browse Jobs", use_container_width=True):
        st.switch_page("pages/2_Apply_for_Jobs.py")