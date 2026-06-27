"""Job recommender using skill overlap scoring."""
import random

JOB_DATABASE = [
    # Data Science
    {"title": "Data Scientist", "company": "TCS", "location": "Bangalore", "salary": "8-14 LPA",
     "skills": ["python", "machine learning", "sql", "pandas", "statistics", "tensorflow"],
     "domain": "Data Science", "experience": "0-2 years", "type": "Full-time"},
    {"title": "ML Engineer", "company": "Infosys", "location": "Hyderabad", "salary": "10-18 LPA",
     "skills": ["python", "pytorch", "deep learning", "nlp", "docker", "aws"],
     "domain": "Machine Learning", "experience": "1-3 years", "type": "Full-time"},
    {"title": "Data Analyst", "company": "Wipro", "location": "Pune", "salary": "5-9 LPA",
     "skills": ["sql", "excel", "tableau", "python", "data analysis"],
     "domain": "Data Science", "experience": "0-2 years", "type": "Full-time"},
    {"title": "AI Research Engineer", "company": "Google", "location": "Hyderabad", "salary": "25-45 LPA",
     "skills": ["python", "tensorflow", "research", "neural network", "bert", "nlp"],
     "domain": "Machine Learning", "experience": "2-5 years", "type": "Full-time"},
    {"title": "Business Intelligence Analyst", "company": "Accenture", "location": "Mumbai", "salary": "6-12 LPA",
     "skills": ["power bi", "sql", "tableau", "excel", "data analysis", "statistics"],
     "domain": "Data Science", "experience": "0-3 years", "type": "Full-time"},
    {"title": "Deep Learning Researcher", "company": "Microsoft", "location": "Hyderabad", "salary": "20-35 LPA",
     "skills": ["pytorch", "python", "neural network", "computer vision", "nlp", "cuda"],
     "domain": "Machine Learning", "experience": "2-5 years", "type": "Full-time"},
    # Web Development
    {"title": "Frontend Developer", "company": "Flipkart", "location": "Bangalore", "salary": "8-15 LPA",
     "skills": ["react", "javascript", "html", "css", "typescript", "rest api"],
     "domain": "Web Development", "experience": "1-3 years", "type": "Full-time"},
    {"title": "Full Stack Developer", "company": "Amazon", "location": "Bangalore", "salary": "15-28 LPA",
     "skills": ["node.js", "react", "python", "aws", "mongodb", "docker"],
     "domain": "Web Development", "experience": "2-4 years", "type": "Full-time"},
    {"title": "Backend Developer", "company": "Zomato", "location": "Gurugram", "salary": "10-18 LPA",
     "skills": ["python", "django", "postgresql", "redis", "docker", "aws"],
     "domain": "Web Development", "experience": "1-3 years", "type": "Full-time"},
    {"title": "React Developer", "company": "Razorpay", "location": "Bangalore", "salary": "12-20 LPA",
     "skills": ["react", "typescript", "javascript", "graphql", "css", "node.js"],
     "domain": "Web Development", "experience": "1-3 years", "type": "Full-time"},
    # Cloud & DevOps
    {"title": "Cloud Engineer", "company": "AWS", "location": "Hyderabad", "salary": "14-24 LPA",
     "skills": ["aws", "terraform", "docker", "kubernetes", "python", "linux"],
     "domain": "Cloud & DevOps", "experience": "1-3 years", "type": "Full-time"},
    {"title": "DevOps Engineer", "company": "Myntra", "location": "Bangalore", "salary": "10-20 LPA",
     "skills": ["docker", "kubernetes", "jenkins", "aws", "linux", "ci/cd"],
     "domain": "Cloud & DevOps", "experience": "1-4 years", "type": "Full-time"},
    {"title": "Site Reliability Engineer", "company": "Swiggy", "location": "Bangalore", "salary": "15-26 LPA",
     "skills": ["kubernetes", "prometheus", "python", "aws", "linux", "docker"],
     "domain": "Cloud & DevOps", "experience": "2-5 years", "type": "Full-time"},
    # Mobile
    {"title": "Android Developer", "company": "Paytm", "location": "Noida", "salary": "8-16 LPA",
     "skills": ["kotlin", "android", "java", "firebase", "rest api"],
     "domain": "Mobile Development", "experience": "1-3 years", "type": "Full-time"},
    {"title": "Flutter Developer", "company": "BYJU's", "location": "Bangalore", "salary": "7-14 LPA",
     "skills": ["flutter", "dart", "firebase", "rest api", "mobile app"],
     "domain": "Mobile Development", "experience": "0-2 years", "type": "Full-time"},
    {"title": "iOS Developer", "company": "OLA", "location": "Bangalore", "salary": "10-18 LPA",
     "skills": ["swift", "ios", "xcode", "firebase", "rest api", "objective-c"],
     "domain": "Mobile Development", "experience": "1-3 years", "type": "Full-time"},
    # Cybersecurity
    {"title": "Security Analyst", "company": "IBM", "location": "Pune", "salary": "8-16 LPA",
     "skills": ["cybersecurity", "network security", "soc", "siem", "python", "linux"],
     "domain": "Cybersecurity", "experience": "1-3 years", "type": "Full-time"},
    {"title": "Penetration Tester", "company": "HCL", "location": "Noida", "salary": "10-18 LPA",
     "skills": ["ethical hacking", "kali", "penetration testing", "python", "vulnerability"],
     "domain": "Cybersecurity", "experience": "1-4 years", "type": "Full-time"},
    # Freshers / Internships
    {"title": "Software Engineer Trainee", "company": "Cognizant", "location": "Chennai", "salary": "4-7 LPA",
     "skills": ["java", "python", "sql", "algorithms", "data structures"],
     "domain": "Software Engineering", "experience": "Fresher", "type": "Full-time"},
    {"title": "Data Science Intern", "company": "Fractal Analytics", "location": "Mumbai", "salary": "25-40k/month",
     "skills": ["python", "pandas", "machine learning", "sql", "statistics"],
     "domain": "Data Science", "experience": "Internship", "type": "Internship"},
    {"title": "ML Intern", "company": "Tiger Analytics", "location": "Chennai", "salary": "20-35k/month",
     "skills": ["python", "scikit-learn", "pandas", "machine learning"],
     "domain": "Machine Learning", "experience": "Internship", "type": "Internship"},
    {"title": "Web Dev Intern", "company": "Internshala", "location": "Remote", "salary": "10-20k/month",
     "skills": ["html", "css", "javascript", "react"],
     "domain": "Web Development", "experience": "Internship", "type": "Internship"},
    {"title": "Associate Software Engineer", "company": "Capgemini", "location": "Hyderabad", "salary": "4-8 LPA",
     "skills": ["java", "python", "sql", "git", "agile"],
     "domain": "Software Engineering", "experience": "Fresher", "type": "Full-time"},
    {"title": "Junior Data Analyst", "company": "Mu Sigma", "location": "Bangalore", "salary": "5-9 LPA",
     "skills": ["sql", "python", "excel", "statistics", "data analysis"],
     "domain": "Data Science", "experience": "0-1 years", "type": "Full-time"},
    {"title": "Product Analyst", "company": "Meesho", "location": "Bangalore", "salary": "8-14 LPA",
     "skills": ["sql", "excel", "python", "data analysis", "tableau", "product"],
     "domain": "Data Science", "experience": "0-2 years", "type": "Full-time"},
]

def get_recommendations(user_skills: list, category: str = '', top_n: int = 10):
    """Return top_n job recommendations sorted by skill match score."""
    user_skills_lower = [s.lower() for s in user_skills]

    scored = []
    for job in JOB_DATABASE:
        job_skills = [s.lower() for s in job['skills']]
        if user_skills_lower:
            match = len(set(user_skills_lower) & set(job_skills))
            total = len(set(user_skills_lower) | set(job_skills))
            score = (match / total * 100) if total > 0 else random.randint(20, 50)
        else:
            score = random.randint(30, 70)

        # Boost if domain matches
        if category and category.lower() in job['domain'].lower():
            score = min(score * 1.3, 99)

        scored.append({**job, 'match_score': round(score, 1)})

    scored.sort(key=lambda x: x['match_score'], reverse=True)
    return scored[:top_n]
