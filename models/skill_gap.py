"""Skill gap analysis between user skills and target role requirements."""

ROLE_SKILLS = {
    'Data Science': {
        'required': ['python', 'pandas', 'numpy', 'sql', 'machine learning', 'statistics',
                     'data visualization', 'scikit-learn', 'matplotlib'],
        'good_to_have': ['tensorflow', 'deep learning', 'tableau', 'power bi', 'spark', 'airflow'],
        'learning_path': ['Start with Python & SQL', 'Learn pandas & numpy', 'Study statistics',
                          'Practice ML with scikit-learn', 'Build 3-5 projects'],
    },
    'Machine Learning': {
        'required': ['python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                     'numpy', 'scikit-learn', 'nlp', 'mathematics'],
        'good_to_have': ['computer vision', 'bert', 'transformers', 'cuda', 'mlops', 'docker'],
        'learning_path': ['Master Python & math foundations', 'Complete ML courses (Andrew Ng)',
                          'Practice on Kaggle', 'Learn PyTorch/TensorFlow', 'Publish projects on GitHub'],
    },
    'Web Development': {
        'required': ['html', 'css', 'javascript', 'react', 'node.js', 'rest api', 'git'],
        'good_to_have': ['typescript', 'next.js', 'graphql', 'docker', 'aws', 'postgresql'],
        'learning_path': ['Learn HTML + CSS basics', 'Master JavaScript', 'Learn React framework',
                          'Study Node.js & Express', 'Build full-stack projects'],
    },
    'Cloud & DevOps': {
        'required': ['linux', 'docker', 'kubernetes', 'aws', 'git', 'ci/cd', 'python'],
        'good_to_have': ['terraform', 'ansible', 'jenkins', 'azure', 'gcp', 'prometheus'],
        'learning_path': ['Learn Linux basics', 'Get AWS/Azure certified', 'Master Docker & Kubernetes',
                          'Study Infrastructure as Code', 'Build DevOps pipelines'],
    },
    'Mobile Development': {
        'required': ['kotlin', 'swift', 'mobile app', 'git', 'rest api', 'firebase'],
        'good_to_have': ['flutter', 'dart', 'android', 'ios', 'react native', 'ci/cd'],
        'learning_path': ['Learn Kotlin (Android) or Swift (iOS)', 'Study Material Design',
                          'Build simple apps', 'Learn Firebase', 'Publish to Play Store / App Store'],
    },
    'Cybersecurity': {
        'required': ['network security', 'linux', 'python', 'cybersecurity', 'ethical hacking'],
        'good_to_have': ['kali', 'penetration testing', 'soc', 'siem', 'vulnerability', 'encryption'],
        'learning_path': ['Study networking fundamentals', 'Learn Linux deeply', 'Get CompTIA Security+',
                          'Practice on HackTheBox / TryHackMe', 'Earn CEH / OSCP'],
    },
    'Software Engineering': {
        'required': ['java', 'python', 'algorithms', 'data structures', 'sql', 'git', 'object-oriented'],
        'good_to_have': ['system design', 'docker', 'microservices', 'agile', 'testing', 'aws'],
        'learning_path': ['Master a language (Java/Python)', 'Study DSA thoroughly',
                          'Practice on LeetCode', 'Learn system design', 'Contribute to open source'],
    },
    'UI/UX Design': {
        'required': ['figma', 'ui', 'ux', 'wireframe', 'prototype', 'user research'],
        'good_to_have': ['adobe xd', 'sketch', 'css', 'html', 'usability testing', 'design system'],
        'learning_path': ['Learn design principles', 'Master Figma', 'Study UX research methods',
                          'Build a portfolio', 'Learn HTML/CSS basics'],
    },
}

def analyze_skill_gap(user_skills: list, target_role: str):
    user_skills_lower = [s.lower() for s in user_skills]

    if target_role not in ROLE_SKILLS:
        # Best match
        target_role = 'Software Engineering'

    role_data = ROLE_SKILLS[target_role]
    required = role_data['required']
    good_to_have = role_data['good_to_have']
    learning_path = role_data['learning_path']

    present_required = [s for s in required if s.lower() in user_skills_lower]
    missing_required = [s for s in required if s.lower() not in user_skills_lower]

    present_gth = [s for s in good_to_have if s.lower() in user_skills_lower]
    missing_gth = [s for s in good_to_have if s.lower() not in user_skills_lower]

    total = len(required)
    readiness = round((len(present_required) / total * 100) if total > 0 else 0)

    return {
        'target_role': target_role,
        'readiness_score': readiness,
        'present_required': present_required,
        'missing_required': missing_required,
        'present_good_to_have': present_gth,
        'missing_good_to_have': missing_gth,
        'learning_path': learning_path,
        'all_roles': list(ROLE_SKILLS.keys()),
    }
