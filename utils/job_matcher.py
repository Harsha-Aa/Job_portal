import streamlit as st
import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    """
    Job matching system that uses NLP to match resumes with job descriptions
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        
        # Common technical skills and keywords
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'laravel'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'nosql'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'spark', 'hadoop', 'tableau'],
            'mobile': ['android', 'ios', 'flutter', 'react native', 'xamarin', 'cordova'],
            'tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello', 'asana']
        }
        
        # Flatten skills list
        self.all_skills = []
        for category, skills in self.technical_skills.items():
            self.all_skills.extend(skills)
    
    def calculate_match_score(self, resume_text: str, job_description: str) -> float:
        """
        Calculate match score between resume and job description
        
        Args:
            resume_text: Text content of resume
            job_description: Job description text
            
        Returns:
            float: Match score as percentage (0-100)
        """
        try:
            if not resume_text or not job_description:
                return 0.0
            
            # Preprocess texts
            resume_clean = self._preprocess_text(resume_text)
            job_clean = self._preprocess_text(job_description)
            
            # Calculate different types of matches
            skill_score = self._calculate_skill_match(resume_clean, job_clean)
            semantic_score = self._calculate_semantic_match(resume_clean, job_clean)
            keyword_score = self._calculate_keyword_match(resume_clean, job_clean)
            
            # Weighted combination
            total_score = (skill_score * 0.4) + (semantic_score * 0.4) + (keyword_score * 0.2)
            
            return min(100.0, max(0.0, total_score))
            
        except Exception as e:
            st.error(f"Error calculating match score: {str(e)}")
            return 0.0
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for matching
        
        Args:
            text: Raw text
            
        Returns:
            str: Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        return text.strip()
    
    def _calculate_skill_match(self, resume_text: str, job_text: str) -> float:
        """
        Calculate skill-based match score
        
        Args:
            resume_text: Preprocessed resume text
            job_text: Preprocessed job description
            
        Returns:
            float: Skill match score (0-100)
        """
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_text)
        
        if not job_skills:
            return 50.0  # Neutral score if no skills in job description
        
        if not resume_skills:
            return 0.0
        
        # Calculate overlap
        matching_skills = set(resume_skills) & set(job_skills)
        skill_match_ratio = len(matching_skills) / len(job_skills)
        
        return skill_match_ratio * 100
    
    def _calculate_semantic_match(self, resume_text: str, job_text: str) -> float:
        """
        Calculate semantic similarity using TF-IDF
        
        Args:
            resume_text: Preprocessed resume text
            job_text: Preprocessed job description
            
        Returns:
            float: Semantic similarity score (0-100)
        """
        try:
            # Create TF-IDF vectors
            documents = [resume_text, job_text]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity * 100
            
        except Exception as e:
            return 0.0
    
    def _calculate_keyword_match(self, resume_text: str, job_text: str) -> float:
        """
        Calculate keyword-based match score
        
        Args:
            resume_text: Preprocessed resume text
            job_text: Preprocessed job description
            
        Returns:
            float: Keyword match score (0-100)
        """
        # Extract important keywords from job description
        job_keywords = self._extract_keywords(job_text)
        
        if not job_keywords:
            return 50.0
        
        # Count matches in resume
        matches = 0
        for keyword in job_keywords:
            if keyword in resume_text:
                matches += 1
        
        return (matches / len(job_keywords)) * 100
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            
        Returns:
            List[str]: List of keywords
        """
        keywords = []
        
        # Common job-related keywords
        job_keywords = [
            'experience', 'years', 'bachelor', 'master', 'degree',
            'certification', 'project', 'team', 'management', 'leadership',
            'development', 'design', 'analysis', 'implementation',
            'communication', 'collaboration', 'problem solving'
        ]
        
        for keyword in job_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        return keywords
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from text
        
        Args:
            text: Input text
            
        Returns:
            List[str]: List of extracted skills
        """
        if not text:
            return []
        
        text = text.lower()
        found_skills = []
        
        # Check for each skill
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                found_skills.append(skill)
        
        # Remove duplicates and sort
        return sorted(list(set(found_skills)))
    
    def get_skill_categories(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize skills by type
        
        Args:
            skills: List of skills
            
        Returns:
            Dict[str, List[str]]: Skills categorized by type
        """
        categorized = {}
        
        for skill in skills:
            skill_lower = skill.lower()
            for category, category_skills in self.technical_skills.items():
                if skill_lower in category_skills:
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(skill)
        
        return categorized
    
    def get_missing_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """
        Get skills required for job but missing from resume
        
        Args:
            resume_skills: Skills found in resume
            job_skills: Skills required for job
            
        Returns:
            List[str]: Missing skills
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        missing = job_set - resume_set
        return sorted(list(missing))
    
    def get_matching_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """
        Get skills that match between resume and job
        
        Args:
            resume_skills: Skills found in resume
            job_skills: Skills required for job
            
        Returns:
            List[str]: Matching skills
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        matching = resume_set & job_set
        return sorted(list(matching))
    
    def generate_match_report(self, resume_text: str, job_description: str) -> Dict:
        """
        Generate comprehensive match report
        
        Args:
            resume_text: Resume text
            job_description: Job description
            
        Returns:
            Dict: Detailed match report
        """
        # Calculate overall score
        match_score = self.calculate_match_score(resume_text, job_description)
        
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        
        # Get skill analysis
        matching_skills = self.get_matching_skills(resume_skills, job_skills)
        missing_skills = self.get_missing_skills(resume_skills, job_skills)
        
        # Categorize skills
        resume_categories = self.get_skill_categories(resume_skills)
        job_categories = self.get_skill_categories(job_skills)
        
        report = {
            'match_score': match_score,
            'resume_skills': resume_skills,
            'job_skills': job_skills,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'resume_skill_categories': resume_categories,
            'job_skill_categories': job_categories,
            'skill_match_percentage': (len(matching_skills) / len(job_skills) * 100) if job_skills else 0,
            'recommendations': self._generate_recommendations(missing_skills, match_score)
        }
        
        return report
    
    def _generate_recommendations(self, missing_skills: List[str], match_score: float) -> List[str]:
        """
        Generate recommendations based on match analysis
        
        Args:
            missing_skills: Skills missing from resume
            match_score: Overall match score
            
        Returns:
            List[str]: Recommendations
        """
        recommendations = []
        
        if match_score < 50:
            recommendations.append("Consider gaining more relevant experience or skills for this role")
        
        if missing_skills:
            top_missing = missing_skills[:5]  # Top 5 missing skills
            recommendations.append(f"Consider learning these skills: {', '.join(top_missing)}")
        
        if match_score > 80:
            recommendations.append("Excellent match! You're well-qualified for this position")
        elif match_score > 60:
            recommendations.append("Good match! Consider highlighting relevant experience")
        
        return recommendations
