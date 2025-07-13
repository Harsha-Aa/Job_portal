"""
Authentication utilities for the job portal
"""
import streamlit as st
from typing import Optional, Dict
from database.database import get_user_by_email, create_user, SessionLocal
from database.models import User
import bcrypt

class AuthManager:
    """Authentication manager for handling user login/logout"""
    
    def __init__(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
    
    def login(self, email: str, password: str) -> bool:
        """
        Authenticate user login
        
        Args:
            email: User email
            password: User password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        user = get_user_by_email(email)
        if user and user.check_password(password) and user.is_active:
            st.session_state.authenticated = True
            st.session_state.user = user.to_dict()
            return True
        return False
    
    def logout(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user"""
        return st.session_state.get('user')
    
    def get_user_role(self) -> str:
        """Get current user role"""
        user = self.get_current_user()
        return user.get('role', 'guest') if user else 'guest'
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.get_user_role() == 'admin'
    
    def is_employer(self) -> bool:
        """Check if current user is employer"""
        return self.get_user_role() == 'employer'
    
    def is_seeker(self) -> bool:
        """Check if current user is seeker"""
        return self.get_user_role() == 'seeker'
    
    def require_auth(self, required_role: str = None):
        """
        Require authentication and optionally specific role
        
        Args:
            required_role: Required user role (admin, employer, seeker)
        """
        if not self.is_authenticated():
            st.error("Please log in to access this page")
            st.switch_page("pages/login.py")
            st.stop()
        
        if required_role and self.get_user_role() != required_role:
            st.error(f"Access denied. This page requires {required_role} role.")
            st.stop()
    
    def register_user(self, user_data: Dict) -> bool:
        """
        Register a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        try:
            # Check if user already exists
            existing_user = get_user_by_email(user_data['email'])
            if existing_user:
                return False
            
            # Create new user
            db = SessionLocal()
            try:
                user = User(
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data.get('role', 'seeker'),
                    phone=user_data.get('phone'),
                    company=user_data.get('company')
                )
                user.set_password(user_data['password'])
                db.add(user)
                db.commit()
                db.refresh(user)
                return True
            finally:
                db.close()
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")
            return False

def show_login_form():
    """Show login form in sidebar"""
    auth = AuthManager()
    
    if auth.is_authenticated():
        user = auth.get_current_user()
        st.sidebar.success(f"Welcome, {user['first_name']}!")
        st.sidebar.write(f"Role: {user['role'].title()}")
        
        if st.sidebar.button("Logout"):
            auth.logout()
            st.rerun()
    else:
        st.sidebar.header("Login")
        
        with st.sidebar.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if auth.login(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Register New Account"):
            st.switch_page("pages/login.py")

def require_role(role: str):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = AuthManager()
            auth.require_auth(role)
            return func(*args, **kwargs)
        return wrapper
    return decorator