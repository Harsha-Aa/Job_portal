# AI-Powered Job Portal

## Overview

This is a comprehensive job portal application built with Streamlit that connects job seekers with employers using AI-powered resume analysis and job matching. The system features job posting capabilities, resume parsing, intelligent job matching, and administrative dashboards.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **UI Components**: Custom CSS styling with Bootstrap-like design
- **Layout**: Multi-page application with sidebar navigation
- **Responsive Design**: Wide layout configuration with column-based responsive design

### Backend Architecture
- **Core Framework**: Python with Streamlit
- **Data Storage**: In-memory storage using Streamlit session state
- **Business Logic**: Modular utility classes for different functionalities
- **File Processing**: PDF and DOCX parsing capabilities

### Key Components
1. **Main Application** (`app.py`) - Entry point and dashboard
2. **Job Postings** (`pages/1_Job_Postings.py`) - Job creation and management
3. **Job Applications** (`pages/2_Apply_for_Jobs.py`) - Job search and application system
4. **Admin Dashboard** (`pages/3_Admin_Dashboard.py`) - Analytics and management interface

## Key Components

### User Authentication System
- **AuthManager Class**: Handles user login, logout, and session management
- **Role-based Access Control**: Three user roles (admin, employer, seeker)
- **Password Security**: Bcrypt hashing for secure password storage
- **Session Management**: Streamlit session state for user persistence

### Data Management
- **Database Backend**: SQLite database with SQLAlchemy ORM for persistent storage
- **User Authentication**: Role-based access control (admin, employer, seeker)
- **DatabaseDataStore Class**: Handles all data operations with database persistence
- **CRUD Operations**: Full create, read, update, delete functionality for jobs, applications, and users

### Resume Processing
- **ResumeParser Class**: Extracts text from PDF and DOCX files
- **File Support**: PDF parsing using PyPDF2, DOCX parsing using python-docx
- **Error Handling**: Comprehensive error handling for unsupported formats

### Job Matching System
- **JobMatcher Class**: AI-powered matching using NLP techniques
- **TF-IDF Vectorization**: Text analysis using scikit-learn
- **Skill Categorization**: Technical skills grouped by categories (programming, web, database, cloud, etc.)
- **Cosine Similarity**: Mathematical matching algorithm for resume-job compatibility

### User Interface
- **Multi-Tab Navigation**: Organized interface with functional tabs
- **Custom Styling**: Bootstrap-inspired CSS for professional appearance
- **Interactive Forms**: Streamlit forms for job posting and applications
- **Data Visualization**: Plotly charts for analytics dashboard

## Data Flow

1. **Job Posting Flow**:
   - Employer fills job posting form
   - Data validation and processing
   - Job stored in session state
   - Confirmation and management interface

2. **Job Application Flow**:
   - Job seeker uploads resume
   - Resume parsing and text extraction
   - Job matching algorithm calculates compatibility scores
   - Application submission and tracking

3. **Admin Management Flow**:
   - Password-protected admin access
   - Analytics dashboard with key metrics
   - Job and application management
   - Data visualization and reporting

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms for job matching

### File Processing
- **PyPDF2**: PDF file parsing
- **python-docx**: Microsoft Word document parsing

### Data Visualization
- **Plotly**: Interactive charts and graphs for analytics

### Utilities
- **UUID**: Unique identifier generation
- **Datetime**: Date and time handling
- **Re**: Regular expressions for text processing

## Deployment Strategy

### Current Architecture
- **Single-file deployment**: Streamlit application with page-based routing
- **Session-based storage**: Data persists during user session only
- **No external database**: All data stored in memory

### Scalability Considerations
- **Database Migration Ready**: DataStore class designed for easy database integration
- **Cloud Deployment**: Compatible with Streamlit Cloud, Heroku, or similar platforms
- **Environment Configuration**: Prepared for environment-specific settings

### Security Features
- **Admin Authentication**: Password-protected administrative functions
- **File Upload Validation**: Secure file processing with format verification
- **Data Sanitization**: Input validation and error handling

## Technical Decisions

### Storage Solution
- **Problem**: Need for data persistence across sessions and users
- **Solution**: SQLite database with SQLAlchemy ORM
- **Rationale**: Persistent storage with minimal setup, supports concurrent users
- **Implementation**: Database models for User, Job, and Application entities with relationships

### Job Matching Algorithm
- **Problem**: Intelligent matching between resumes and job descriptions
- **Solution**: TF-IDF vectorization with cosine similarity
- **Rationale**: Proven NLP technique for text similarity
- **Alternatives**: More advanced ML models, neural networks for semantic matching

### File Processing
- **Problem**: Support multiple resume formats
- **Solution**: Separate parsers for PDF and DOCX
- **Rationale**: Most common resume formats in professional settings
- **Limitations**: No support for images, scanned documents, or other formats

### UI Framework Choice
- **Problem**: Rapid development of interactive web application
- **Solution**: Streamlit framework with custom CSS
- **Rationale**: Python-native, rapid prototyping, built-in components
- **Trade-offs**: Limited customization compared to React/Vue, but faster development