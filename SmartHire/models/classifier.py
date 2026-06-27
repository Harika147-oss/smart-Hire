"""Resume category classifier using keyword scoring."""

DOMAIN_KEYWORDS = {
    'Data Science': [
        'data science', 'machine learning', 'deep learning', 'python', 'pandas', 'numpy',
        'statistics', 'data analysis', 'tensorflow', 'pytorch', 'scikit-learn', 'sql',
        'visualization', 'tableau', 'power bi', 'nlp', 'ai', 'neural network', 'xgboost'
    ],
    'Web Development': [
        'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
        'django', 'flask', 'rest api', 'graphql', 'bootstrap', 'tailwind', 'next.js',
        'frontend', 'backend', 'fullstack', 'responsive', 'web design'
    ],
    'Machine Learning': [
        'machine learning', 'deep learning', 'neural network', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'keras', 'model training', 'feature engineering',
        'classification', 'regression', 'clustering', 'reinforcement learning', 'bert'
    ],
    'Cloud & DevOps': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'devops',
        'jenkins', 'linux', 'ansible', 'cloud', 'microservices', 'serverless', 'pipeline'
    ],
    'Mobile Development': [
        'android', 'ios', 'flutter', 'react native', 'kotlin', 'swift', 'dart',
        'mobile app', 'xcode', 'android studio', 'firebase', 'mobile development'
    ],
    'Cybersecurity': [
        'cybersecurity', 'network security', 'ethical hacking', 'penetration testing',
        'firewall', 'encryption', 'soc', 'vulnerability', 'malware', 'oscp', 'kali'
    ],
    'Database Administration': [
        'sql', 'postgresql', 'mysql', 'oracle', 'mongodb', 'redis', 'nosql',
        'database', 'dba', 'query optimization', 'indexing', 'stored procedure'
    ],
    'UI/UX Design': [
        'ui', 'ux', 'figma', 'sketch', 'adobe xd', 'user interface', 'user experience',
        'wireframe', 'prototype', 'design system', 'usability', 'accessibility'
    ],
    'Software Engineering': [
        'software development', 'java', 'c++', 'c#', 'algorithms', 'data structures',
        'object-oriented', 'system design', 'design patterns', 'agile', 'scrum', 'testing'
    ],
    'Business Analyst': [
        'business analysis', 'requirements gathering', 'stakeholder', 'process improvement',
        'jira', 'confluence', 'excel', 'powerpoint', 'documentation', 'use case', 'workflow'
    ],
}

def predict_category(text: str):
    text_lower = text.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[domain] = score

    if max(scores.values()) == 0:
        return 'Software Engineering', 0.5, scores

    total = sum(scores.values())
    best = max(scores, key=scores.get)
    confidence = scores[best] / total if total > 0 else 0.5

    # Normalize to probabilities
    probs = {k: v / total if total > 0 else 0 for k, v in scores.items()}
    return best, round(confidence, 2), probs

def get_all_domains():
    return list(DOMAIN_KEYWORDS.keys())
