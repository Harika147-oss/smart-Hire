import streamlit as st
import os, sys, time, json
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import get_css
from utils.auth import check_auth, login_user, register_user, logout, get_current_user, update_user
from utils.resume_parser import (parse_resume, extract_skills, extract_education,
                                  extract_experience, compute_resume_score, extract_email, extract_phone)
from models.classifier import predict_category
from models.recommender import get_recommendations
from models.skill_gap import analyze_skill_gap

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartHire – AI Career Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(get_css(), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION DEFAULTS
# ─────────────────────────────────────────────
for key, default in {
    'current_page': 'dashboard',
    'resume_text': '',
    'extracted_skills': [],
    'resume_score': 0,
    'job_match': 0,
    'analysis_done': False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def nav_to(page: str):
    st.session_state.current_page = page
    st.rerun()

def card(content: str):
    st.markdown(f'<div class="card">{content}</div>', unsafe_allow_html=True)

def metric_card(icon, value, label, color="purple"):
    st.markdown(f"""
    <div class="metric-card metric-{color}">
        <span class="metric-icon">{icon}</span>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)

def skill_tags(skills, missing=False):
    cls = "skill-tag-missing" if missing else "skill-tag"
    return "".join(f'<span class="{cls}">{s.title()}</span>' for s in skills)

# ─────────────────────────────────────────────
#  EXAM QUESTIONS
# ─────────────────────────────────────────────
EXAM_QUESTIONS = {
    "Easy": [
        {"q": "What is the output of: print(bool(\"False\")) in Python?",
         "opts": ["False", "True", "Error", "None"], "ans": "True",
         "exp": "Any non-empty string is truthy in Python, even the string \"False\"."},
        {"q": "What is the time complexity of accessing an element by index in an array?",
         "opts": ["O(n)", "O(log n)", "O(1)", "O(n²)"], "ans": "O(1)",
         "exp": "Arrays support direct index access in constant time O(1)."},
        {"q": "Which data structure follows LIFO (Last In First Out) principle?",
         "opts": ["Queue", "Heap", "Stack", "Linked List"], "ans": "Stack",
         "exp": "Stack follows LIFO — the last element pushed is the first to be popped."},
        {"q": "In SQL, which clause is used to filter results after GROUP BY?",
         "opts": ["WHERE", "ORDER BY", "HAVING", "FILTER"], "ans": "HAVING",
         "exp": "HAVING filters grouped results; WHERE filters individual rows before grouping."},
        {"q": "What is the output of: print(10 % 3)?",
         "opts": ["3", "1", "0", "3.33"], "ans": "1",
         "exp": "10 % 3 = 1 (remainder when 10 is divided by 3)."},
        {"q": "What is the output of: print(len([1, [2, 3], 4]))?",
         "opts": ["2", "3", "4", "Error"], "ans": "3",
         "exp": "The list has 3 elements: 1, [2,3] (a nested list counts as 1), and 4."},
        {"q": "In OOP, what does Encapsulation mean?",
         "opts": ["Inheriting from a parent class", "Hiding implementation details inside a class",
                  "Creating multiple instances", "Overriding parent methods"], "ans": "Hiding implementation details inside a class",
         "exp": "Encapsulation bundles data and methods and hides internal implementation."},
        {"q": "What port does HTTPS use by default?",
         "opts": ["80", "21", "443", "8080"], "ans": "443",
         "exp": "HTTPS (secure HTTP) uses port 443 by default; HTTP uses port 80."},
        {"q": "What is the decimal value of binary number 1010?",
         "opts": ["8", "9", "10", "12"], "ans": "10",
         "exp": "1010 in binary = 1×8 + 0×4 + 1×2 + 0×1 = 10."},
        {"q": "x = 5; y = x; y = 10; print(x) — What is printed?",
         "opts": ["10", "5", "Error", "None"], "ans": "5",
         "exp": "Integers are immutable; y = 10 rebinds y but doesn't change x."},
    ],
    "Medium": [
        {"q": "What is the worst-case time complexity of QuickSort?",
         "opts": ["O(n log n)", "O(n²)", "O(n)", "O(n³)"], "ans": "O(n²)",
         "exp": "QuickSort degrades to O(n²) when the pivot is always the smallest or largest element (already sorted array)."},
        {"q": "What does ACID stand for in databases?",
         "opts": ["Access, Consistency, Isolation, Durability",
                  "Atomicity, Consistency, Isolation, Durability",
                  "Atomicity, Correctness, Integrity, Durability",
                  "Atomicity, Coordination, Isolation, Data"], "ans": "Atomicity, Consistency, Isolation, Durability",
         "exp": "ACID guarantees reliable database transactions: Atomicity, Consistency, Isolation, Durability."},
        {"q": "l = [1,2,3]; m = l[:]; m.append(4); print(len(l)) — Output?",
         "opts": ["3", "4", "7", "Error"], "ans": "3",
         "exp": "l[:] creates a shallow copy. Appending to m does not affect l, so len(l) = 3."},
        {"q": "Which sorting algorithm works best for sorting a Linked List?",
         "opts": ["QuickSort", "HeapSort", "Merge Sort", "Radix Sort"], "ans": "Merge Sort",
         "exp": "Merge Sort is ideal for linked lists — it doesn't require random access and has O(n log n) complexity."},
        {"q": "What is the space complexity of a recursive DFS on a tree of height h?",
         "opts": ["O(1)", "O(log n)", "O(h)", "O(n²)"], "ans": "O(h)",
         "exp": "Recursive DFS uses the call stack which goes as deep as the tree height h."},
        {"q": "What is a deadlock in an operating system?",
         "opts": ["A process running for too long", "Circular wait where processes hold resources needed by each other",
                  "Memory overflow", "CPU overload"], "ans": "Circular wait where processes hold resources needed by each other",
         "exp": "Deadlock occurs when processes wait circularly for resources — none can proceed."},
        {"q": "Which HTTP method is idempotent but NOT safe?",
         "opts": ["GET", "HEAD", "PUT", "POST"], "ans": "PUT",
         "exp": "PUT is idempotent (same result on multiple calls) but not safe (it modifies server state). GET/HEAD are both safe and idempotent."},
        {"q": "O(2^n) belongs to which complexity class?",
         "opts": ["Polynomial", "Logarithmic", "Exponential", "Linear"], "ans": "Exponential",
         "exp": "2^n grows exponentially — algorithms with this complexity are impractical for large inputs."},
        {"q": "What is the time complexity of inserting into a Min-Heap?",
         "opts": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "ans": "O(log n)",
         "exp": "Heap insertion adds at the end then bubbles up — takes O(log n) in worst case."},
        {"q": "Which of the following is NOT a valid HTTP request method?",
         "opts": ["GET", "POST", "FIND", "DELETE"], "ans": "FIND",
         "exp": "Standard HTTP methods are GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. FIND does not exist."},
    ],
    "Hard": [
        {"q": "What is the time complexity of building a Max-Heap from an unsorted array of n elements?",
         "opts": ["O(n log n)", "O(n)", "O(log n)", "O(n²)"], "ans": "O(n)",
         "exp": "Using bottom-up heapification (Floyd's algorithm), a heap can be built in O(n) — counterintuitively faster than O(n log n)."},
        {"q": "In the CAP theorem, which statement is correct?",
         "opts": ["A distributed system can guarantee all three: Consistency, Availability, Partition Tolerance",
                  "A distributed system can guarantee at most two of: Consistency, Availability, Partition Tolerance",
                  "Partition Tolerance is optional in modern systems",
                  "Consistency always takes priority over Availability"], "ans": "A distributed system can guarantee at most two of: Consistency, Availability, Partition Tolerance",
         "exp": "CAP theorem states: during a network partition you must choose between Consistency and Availability."},
        {"q": "What is the time complexity of Dijkstra's algorithm using a Binary Min-Heap?",
         "opts": ["O(V²)", "O(E log V)", "O((V + E) log V)", "O(V log E)"], "ans": "O((V + E) log V)",
         "exp": "Each vertex is extracted once O(V log V) and each edge relaxation takes O(log V), giving O((V+E) log V)."},
        {"q": "What is the amortized time complexity of push() in a dynamic array using doubling strategy?",
         "opts": ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "ans": "O(1)",
         "exp": "Though occasional resizes cost O(n), the amortized cost per push is O(1) — total work across n pushes is O(n)."},
        {"q": "A server receives 1000 requests/sec. Each request takes 100ms to process. What is the minimum number of servers needed?",
         "opts": ["10", "100", "50", "1000"], "ans": "100",
         "exp": "Each server handles 1/0.1 = 10 req/s. To handle 1000 req/s you need 1000/10 = 100 servers (Little's Law: L = λW)."},
        {"q": "Which regularization technique produces sparse models by forcing some weights to exactly zero?",
         "opts": ["L2 Regularization (Ridge)", "Dropout", "L1 Regularization (Lasso)", "Batch Normalization"], "ans": "L1 Regularization (Lasso)",
         "exp": "L1 (Lasso) regularization adds |w| penalty, which geometrically drives sparse solutions with exact zeros. L2 shrinks but rarely zeroes."},
        {"q": "What is the primary advantage of B+ Trees over B Trees for database indexing?",
         "opts": ["Lower tree height", "All data stored in leaf nodes enabling efficient sequential/range queries",
                  "Faster insertion", "Less memory usage"], "ans": "All data stored in leaf nodes enabling efficient sequential/range queries",
         "exp": "B+ Trees store all data in leaf nodes linked sequentially — perfect for range queries and full scans without traversing internal nodes."},
        {"q": "Which of these is proven to be NP-Complete?",
         "opts": ["Sorting a list", "Binary Search", "Travelling Salesman Problem (decision version)", "BFS traversal"], "ans": "Travelling Salesman Problem (decision version)",
         "exp": "TSP (decision: 'is there a tour of cost ≤ k?') is NP-Complete. Optimization TSP is NP-Hard. Sorting/Search/BFS are polynomial."},
        {"q": "The Bellman-Ford algorithm is based on which algorithmic paradigm?",
         "opts": ["Greedy", "Divide and Conquer", "Dynamic Programming", "Backtracking"], "ans": "Dynamic Programming",
         "exp": "Bellman-Ford relaxes edges repeatedly (V-1 times), building up shortest paths — a classic DP approach on graphs."},
        {"q": "In SQL, which isolation level prevents Phantom Reads?",
         "opts": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"], "ans": "Serializable",
         "exp": "Serializable is the highest isolation level — it prevents dirty reads, non-repeatable reads, AND phantom reads by serializing transactions."},
    ],
}

# ─────────────────────────────────────────────
#  LOGIN / SIGNUP PAGE
# ─────────────────────────────────────────────
def show_login_page():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    section.main > div { padding-top: 0 !important; }
    </style>""", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
        <div class="login-hero">
            <div class="login-hero-icon">🎓</div>
            <h1>SmartHire</h1>
            <p>AI-Powered Career Guidance Platform</p>
        </div>""", unsafe_allow_html=True)

        # Student image
        img_path = os.path.join(os.path.dirname(__file__), 'assets', 'student.png')
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔐  Login", "✨  Sign Up"])

        # ── LOGIN ──
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                email    = st.text_input("📧  Email Address", placeholder="you@email.com")
                password = st.text_input("🔒  Password", type="password", placeholder="Enter your password")
                col1, col2 = st.columns([2, 1])
                with col1:
                    submit = st.form_submit_button("Login →", use_container_width=True)
                if submit:
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        ok, user = login_user(email, password)
                        if ok:
                            st.session_state['logged_in'] = True
                            st.session_state['user']      = user
                            st.session_state['email']     = user['email']
                            st.session_state['current_page'] = 'dashboard'
                            st.success("Welcome back! Loading your dashboard…")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Incorrect email or password.")
            st.markdown("""<div style="text-align:center;color:#64748b;font-size:0.8rem;margin-top:8px;">
                Demo: register first, then login</div>""", unsafe_allow_html=True)

        # ── SIGN UP ──
        with tab_signup:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("signup_form", clear_on_submit=False):
                s_name  = st.text_input("👤  Full Name", placeholder="Rahul Sharma")
                s_email = st.text_input("📧  Email", placeholder="rahul@email.com")
                s_col   = st.text_input("🏫  College / University", placeholder="IIT Bombay")
                s_domain = st.selectbox("🎯  Target Domain", [
                    "Data Science", "Machine Learning", "Web Development",
                    "Cloud & DevOps", "Mobile Development",
                    "Cybersecurity", "Software Engineering", "UI/UX Design"])
                s_year  = st.selectbox("📅  Year of Study", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate"])
                s_pass  = st.text_input("🔒  Password", type="password", placeholder="Min 6 characters")
                s_conf  = st.text_input("🔒  Confirm Password", type="password", placeholder="Repeat password")
                reg = st.form_submit_button("Create Account →", use_container_width=True)
                if reg:
                    if not all([s_name, s_email, s_pass, s_conf]):
                        st.error("Please fill all required fields.")
                    elif len(s_pass) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif s_pass != s_conf:
                        st.error("Passwords do not match.")
                    else:
                        ok, msg = register_user(s_name, s_email, s_pass, s_col, s_domain, s_year)
                        if ok:
                            st.success("Account created! Switch to Login tab.")
                        else:
                            st.error(msg)

        # Features list
        st.markdown("""
        <div style="margin-top:24px;">
            <div class="feature-item"><span>✅</span><span>AI-powered resume analysis</span></div>
            <div class="feature-item"><span>✅</span><span>Smart job recommendations</span></div>
            <div class="feature-item"><span>✅</span><span>Skill gap identification</span></div>
            <div class="feature-item"><span>✅</span><span>Placement preparation exams</span></div>
            <div class="feature-item"><span>✅</span><span>Personalized learning resources</span></div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def show_sidebar():
    user = get_current_user() or {}
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🎓 SmartHire</h2>
            <p>AI Career Guidance Platform</p>
        </div>""", unsafe_allow_html=True)

        # User card
        st.markdown(f"""
        <div class="sidebar-user">
            <div class="sidebar-user-avatar">👨‍🎓</div>
            <div>
                <div class="sidebar-user-name">{user.get('name','User')}</div>
                <div class="sidebar-user-email">{user.get('email','')}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">MAIN MENU</div>', unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Dashboard",           "dashboard"),
            ("📄", "Resume Upload",        "resume_upload"),
            ("🔍", "Resume Analysis",      "resume_analysis"),
            ("💼", "Job Recommendations",  "jobs"),
            ("📊", "Skill Gap Report",     "skill_gap"),
            ("📝", "Exams",               "exams"),
            ("📚", "Learning Resources",   "learning"),
        ]
        for icon, label, page_id in nav_items:
            active = "✦ " if st.session_state.current_page == page_id else "   "
            if st.button(f"{icon}  {active}{label}", key=f"nav_{page_id}"):
                st.session_state.current_page = page_id
                st.rerun()

        st.markdown('<div class="sidebar-section">ACCOUNT</div>', unsafe_allow_html=True)

        for icon, label, page_id in [("👤", "Profile", "profile"), ("ℹ️", "About", "about")]:
            active = "✦ " if st.session_state.current_page == page_id else "   "
            if st.button(f"{icon}  {active}{label}", key=f"nav_{page_id}"):
                st.session_state.current_page = page_id
                st.rerun()

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        if st.button("🚪  Logout", key="nav_logout"):
            logout()
            st.rerun()

# ─────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────

# ── DASHBOARD ──
def page_dashboard():
    user = get_current_user() or {}
    name = user.get('name', 'Student')

    st.markdown(f"""
    <div class="welcome-banner">
        <h1>Welcome back, {name.split()[0]}! 👋</h1>
        <p>Track your career progress, upload your resume, and prepare for placements.</p>
    </div>""", unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("📋", f"{user.get('resume_score', 0)}%", "Resume Score", "purple")
    with c2: metric_card("💼", f"{user.get('job_match', 0)}%",   "Job Match",    "blue")
    with c3: metric_card("📝", user.get('exams_taken', 0),        "Tests Taken",  "green")
    with c4: metric_card("📌", user.get('assignments', 0),        "Assignments",  "orange")
    with c5: metric_card("🏆", f"{user.get('highest_score', 0)}%","Highest Score","pink")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Skill Gap preview
        st.markdown('<div class="section-title">📊 Skill Gap Overview</div>', unsafe_allow_html=True)
        domain = user.get('domain', 'Data Science')
        gap = analyze_skill_gap(user.get('skills', []), domain)
        skills_data = {
            "Python": 75, "Machine Learning": 60, "SQL": 80,
            "Deep Learning": 40, "Data Visualization": 65,
        }
        for skill, pct in skills_data.items():
            color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:0.85rem;color:#e2e8f0;">{skill}</span>
                    <span style="font-size:0.85rem;color:#94a3b8;">{pct}%</span>
                </div>
                <div style="background:#1e293b;border-radius:999px;height:7px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:999px;transition:width 0.6s;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        if st.button("📊 View Full Report", key="dash_skillgap"):
            nav_to("skill_gap")

    with col_b:
        # Recommended domain
        st.markdown('<div class="section-title">🎯 Recommended Domain</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div style="font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:8px;">
                {user.get('domain','Data Science')}
            </div>
            <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:12px;">
                Based on your profile and skills
            </div>
            <div style="margin-bottom:10px;font-size:0.85rem;color:#c4b5fd;font-weight:600;">Top Skills to Learn:</div>
        """, unsafe_allow_html=True)
        for s in ["Python", "Machine Learning", "SQL", "TensorFlow"]:
            st.markdown(f'<span class="skill-tag">{s}</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Upcoming exams
        st.markdown('<div class="section-title" style="margin-top:16px;">📝 Quick Exam Access</div>', unsafe_allow_html=True)
        for diff, color, icon in [("Easy","#10b981","🟢"), ("Medium","#f59e0b","🟡"), ("Hard","#ef4444","🔴")]:
            c = st.columns([4, 1])
            with c[0]:
                st.markdown(f'<span style="color:{color};font-weight:600;">{icon} {diff} Level</span>', unsafe_allow_html=True)
            with c[1]:
                if st.button("Start", key=f"dash_exam_{diff}"):
                    st.session_state['exam_diff'] = diff
                    nav_to("exams")

    # Career insights
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Career Insights</div>', unsafe_allow_html=True)
    ci1, ci2, ci3 = st.columns(3)
    insights = [
        ("💰", "Salary Range",  "₹8 – 20 LPA",   "For your target domain", "blue"),
        ("📈", "Market Demand", "Very High",       "1000+ openings / month", "green"),
        ("🚀", "Growth Rate",   "35% YoY",         "Industry growing fast",  "orange"),
    ]
    for col, (icon, title, val, sub, color) in zip([ci1, ci2, ci3], insights):
        with col:
            metric_card(icon, val, f"{title} — {sub}", color)


# ── RESUME UPLOAD ──
def page_resume_upload():
    page_header("📄 Resume Upload", "Upload your resume and let AI extract insights")

    col_upload, col_info = st.columns([3, 2])
    with col_upload:
        st.markdown("""
        <div class="card">
            <div class="section-title">📁 Upload Resume</div>
            <p style="color:#94a3b8;font-size:0.85rem;margin-bottom:16px;">
                Supported formats: PDF, DOCX, TXT
            </p>
        </div>""", unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop your resume here or click to browse",
            type=["pdf", "docx", "doc", "txt"],
            label_visibility="collapsed"
        )

        if uploaded:
            with st.spinner("Parsing your resume…"):
                text = parse_resume(uploaded)
                skills  = extract_skills(text)
                edu     = extract_education(text)
                exp     = extract_experience(text)
                score   = compute_resume_score(skills, edu, exp, text)

                st.session_state['resume_text']     = text
                st.session_state['extracted_skills']= skills
                st.session_state['resume_score']    = score
                st.session_state['analysis_done']   = True

                user_email = st.session_state.get('email', '')
                if user_email:
                    update_user(user_email, {
                        'skills': skills,
                        'resume_score': score,
                        'resume_text': text[:500],
                    })

            st.success(f"✅ Resume parsed successfully! Score: **{score}/100**")

            tab_text, tab_skills, tab_edu = st.tabs(["📝 Raw Text", "🔧 Skills", "🎓 Education"])

            with tab_text:
                st.text_area("Extracted text", text[:2000] + ("…" if len(text) > 2000 else ""),
                             height=250, disabled=True)

            with tab_skills:
                if skills:
                    st.markdown("**Detected Skills:**")
                    st.markdown(skill_tags(skills), unsafe_allow_html=True)
                else:
                    st.info("No recognised skills detected. Try a more detailed resume.")

            with tab_edu:
                if edu:
                    for e in edu:
                        st.markdown(f"🎓 {e}")
                else:
                    st.info("No education entries detected.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Go to Resume Analysis →", use_container_width=True):
                nav_to("resume_analysis")

    with col_info:
        st.markdown("""
        <div class="card">
            <div class="section-title">💡 Tips for a Great Resume</div>
        </div>""", unsafe_allow_html=True)
        tips = [
            ("📌", "Use action verbs (Built, Designed, Led, Improved)"),
            ("📌", "Quantify achievements (e.g. Improved accuracy by 15%)"),
            ("📌", "List skills explicitly in a dedicated section"),
            ("📌", "Include GitHub / portfolio links"),
            ("📌", "Keep it 1–2 pages max"),
            ("📌", "Use standard fonts and clear formatting"),
        ]
        for icon, tip in tips:
            st.markdown(f"""
            <div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1e293b;align-items:flex-start;">
                <span>{icon}</span>
                <span style="font-size:0.85rem;color:#94a3b8;">{tip}</span>
            </div>""", unsafe_allow_html=True)

        score = st.session_state.get('resume_score', 0)
        if score:
            st.markdown("<br>", unsafe_allow_html=True)
            color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
            label = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Work"
            st.markdown(f"""
            <div class="metric-card" style="margin-top:10px;">
                <div class="metric-icon">📋</div>
                <div class="metric-value" style="color:{color};">{score}</div>
                <div class="metric-label">Resume Score — {label}</div>
            </div>""", unsafe_allow_html=True)


# ── RESUME ANALYSIS ──
def page_resume_analysis():
    page_header("🔍 Resume Analysis", "AI-powered analysis of your resume using ML")

    if not st.session_state.get('analysis_done'):
        st.info("📄 Please upload your resume first.")
        if st.button("Go to Resume Upload →"):
            nav_to("resume_upload")
        return

    text   = st.session_state.get('resume_text', '')
    skills = st.session_state.get('extracted_skills', [])
    score  = st.session_state.get('resume_score', 0)

    # Classify
    category, confidence, probs = predict_category(text)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        # Score ring
        color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:30px;">
            <div style="font-size:0.9rem;color:#94a3b8;margin-bottom:8px;">Overall Resume Score</div>
            <div style="font-size:5rem;font-weight:900;color:{color};line-height:1;">{score}</div>
            <div style="font-size:0.8rem;color:#64748b;">out of 100</div>
        </div>""", unsafe_allow_html=True)

        # Predicted domain
        st.markdown(f"""
        <div class="card" style="margin-top:16px;">
            <div class="section-title">🎯 Predicted Domain</div>
            <div style="font-size:1.3rem;font-weight:700;color:#a78bfa;margin:8px 0;">{category}</div>
            <div style="font-size:0.85rem;color:#94a3b8;">Confidence: {confidence*100:.0f}%</div>
        </div>""", unsafe_allow_html=True)

        # Top 5 domain match
        st.markdown('<div class="section-title" style="margin-top:18px;">📊 Domain Match Scores</div>', unsafe_allow_html=True)
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5]
        for dom, prob in sorted_probs:
            pct = int(prob * 100)
            bar_color = "#7c3aed" if dom == category else "#2563eb"
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="font-size:0.82rem;color:#e2e8f0;">{dom}</span>
                    <span style="font-size:0.82rem;color:#94a3b8;">{pct}%</span>
                </div>
                <div style="background:#1e293b;border-radius:999px;height:7px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:999px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        # Skills breakdown
        skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in skills[:20]) if skills else '<p style="color:#64748b;font-size:0.85rem;">No skills detected</p>'
        st.markdown(f'<div class="card"><div class="section-title">🔧 Detected Skills ({len(skills)})</div>{skills_html}</div>', unsafe_allow_html=True)

        # Score breakdown
        st.markdown("""
        <div class="card" style="margin-top:16px;">
            <div class="section-title">📈 Score Breakdown</div>
        </div>""", unsafe_allow_html=True)
        breakdown = [
            ("Skills", min(len(skills)*4, 40), 40, "#7c3aed"),
            ("Education", 20, 20, "#2563eb"),
            ("Experience", 24, 24, "#10b981"),
            ("Content", 8, 8, "#f59e0b"),
            ("Contact Info", 8, 8, "#ec4899"),
        ]
        for label, val, total, color in breakdown:
            pct = int(val / total * 100) if total else 0
            st.markdown(f"""
            <div style="margin-bottom:9px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
                    <span style="font-size:0.82rem;color:#e2e8f0;">{label}</span>
                    <span style="font-size:0.82rem;color:#94a3b8;">{val}/{total}</span>
                </div>
                <div style="background:#1e293b;border-radius:999px;height:6px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:999px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💼 View Job Recommendations →", use_container_width=True):
        nav_to("jobs")


# ── JOB RECOMMENDATIONS ──
def page_jobs():
    page_header("💼 Job Recommendations", "Personalized job matches based on your skills")

    user   = get_current_user() or {}
    skills = st.session_state.get('extracted_skills') or user.get('skills', [])
    domain = user.get('domain', '')

    # Filters row
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1:
        filter_type = st.selectbox("Job Type", ["All", "Full-time", "Internship"], key="jf_type")
    with col_f2:
        filter_domain = st.selectbox("Domain", ["All"] + [
            "Data Science", "Machine Learning", "Web Development",
            "Cloud & DevOps", "Mobile Development", "Cybersecurity", "Software Engineering"
        ], key="jf_domain")
    with col_f3:
        top_n = st.selectbox("Show", [5, 10, 15, 20], index=1, key="jf_n")

    jobs = get_recommendations(skills, domain, top_n=top_n)

    # Apply filters
    if filter_type != "All":
        jobs = [j for j in jobs if j.get('type', '') == filter_type]
    if filter_domain != "All":
        jobs = [j for j in jobs if filter_domain.lower() in j.get('domain', '').lower()]

    st.markdown(f'<div style="color:#94a3b8;font-size:0.85rem;margin-bottom:14px;">Showing {len(jobs)} matching jobs</div>', unsafe_allow_html=True)

    col_list, col_detail = st.columns([3, 2])
    with col_list:
        for i, job in enumerate(jobs):
            score = job.get('match_score', 0)
            color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
            with st.expander(f"{'🏆 ' if score>=80 else ''}  {job['title']} — {job['company']}  |  {job['match_score']}% match", expanded=(i==0)):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"""
                    <div class="job-title">{job['title']}</div>
                    <div class="job-company">🏢 {job['company']}  📍 {job['location']}  ⏰ {job['experience']}</div>
                    <div style="margin:10px 0;">
                        <span class="badge badge-blue">{job.get('type','Full-time')}</span>
                        <span class="badge badge-purple" style="margin-left:6px;">{job.get('domain','')}</span>
                    </div>
                    <div style="font-size:0.85rem;color:#94a3b8;margin:6px 0;">
                        💰 {job['salary']}
                    </div>
                    <div style="margin-top:10px;">
                        {"".join(f'<span class="skill-tag">{s.title()}</span>' for s in job.get('skills',[])[:6])}
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div style="text-align:center;padding:16px;">
                        <div style="font-size:2rem;font-weight:900;color:{color};">{score:.0f}%</div>
                        <div style="font-size:0.75rem;color:#94a3b8;">Match Score</div>
                    </div>""", unsafe_allow_html=True)
                    st.button("Apply Now 🚀", key=f"apply_{i}", use_container_width=True)

    with col_detail:
        st.markdown("""
        <div class="card">
            <div class="section-title">📈 Market Overview</div>
            <div style="color:#94a3b8;font-size:0.85rem;">
                Top hiring companies in your domain:
            </div>
        </div>""", unsafe_allow_html=True)
        companies = ["TCS", "Infosys", "Wipro", "Amazon", "Google", "Microsoft", "Flipkart", "Swiggy"]
        for c in companies:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px;background:#0f172a;border-radius:8px;margin-bottom:6px;">
                <span style="font-size:1.2rem;">🏢</span>
                <span style="font-size:0.85rem;color:#e2e8f0;font-weight:500;">{c}</span>
                <span class="badge badge-green" style="margin-left:auto;">Hiring</span>
            </div>""", unsafe_allow_html=True)


# ── SKILL GAP ──
def page_skill_gap():
    page_header("📊 Skill Gap Report", "Identify what skills you need to land your dream job")

    user   = get_current_user() or {}
    skills = st.session_state.get('extracted_skills') or user.get('skills', [])
    domain = user.get('domain', 'Data Science')

    # Role selector
    from models.skill_gap import ROLE_SKILLS
    roles = list(ROLE_SKILLS.keys())
    target = st.selectbox("🎯 Target Role", roles,
                          index=roles.index(domain) if domain in roles else 0)

    gap = analyze_skill_gap(skills, target)

    col_score, col_main = st.columns([1, 3])
    with col_score:
        score = gap['readiness_score']
        color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        label = "Job Ready!" if score >= 80 else "Almost There" if score >= 60 else "Keep Learning"
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:28px 16px;">
            <div style="font-size:0.85rem;color:#94a3b8;margin-bottom:8px;">Readiness Score</div>
            <div style="font-size:3.5rem;font-weight:900;color:{color};line-height:1;">{score}%</div>
            <div style="font-size:0.8rem;color:{color};margin-top:8px;font-weight:600;">{label}</div>
        </div>""", unsafe_allow_html=True)

    with col_main:
        tab_missing, tab_present, tab_path = st.tabs(["❌ Missing Skills", "✅ Your Skills", "🗺️ Learning Path"])

        with tab_missing:
            if gap['missing_required']:
                st.markdown("**Critical Skills to Learn:**")
                st.markdown(skill_tags(gap['missing_required'], missing=True), unsafe_allow_html=True)
            else:
                st.success("🎉 You have all required skills!")
            if gap['missing_good_to_have']:
                st.markdown("<br>**Good to Have:**", unsafe_allow_html=True)
                st.markdown(skill_tags(gap['missing_good_to_have'], missing=True), unsafe_allow_html=True)

            # Progress bars for each required skill
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("**Skill Coverage:**")
            all_req = gap['missing_required'] + gap['present_required']
            for sk in all_req:
                has = sk in gap['present_required']
                pct = 100 if has else 0
                color = "#10b981" if has else "#ef4444"
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="font-size:0.82rem;color:#e2e8f0;">{sk.title()}</span>
                        <span style="font-size:0.75rem;color:{'#10b981' if has else '#ef4444'};">{'✓ Have it' if has else '✗ Missing'}</span>
                    </div>
                    <div style="background:#1e293b;border-radius:999px;height:6px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{color};border-radius:999px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        with tab_present:
            if gap['present_required']:
                st.markdown("**Skills You Already Have:**")
                st.markdown(skill_tags(gap['present_required']), unsafe_allow_html=True)
            if gap['present_good_to_have']:
                st.markdown("<br>**Bonus Skills:**", unsafe_allow_html=True)
                st.markdown(skill_tags(gap['present_good_to_have']), unsafe_allow_html=True)
            if not gap['present_required'] and not gap['present_good_to_have']:
                st.info("Upload your resume first to see your current skills.")

        with tab_path:
            st.markdown("**📍 Recommended Learning Path:**")
            for i, step in enumerate(gap['learning_path'], 1):
                color = "#7c3aed" if i == 1 else "#2563eb" if i == 2 else "#10b981" if i <= 4 else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:12px;background:#0f172a;border-radius:10px;margin-bottom:8px;border-left:3px solid {color};">
                    <span style="background:{color};color:#fff;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;flex-shrink:0;">{i}</span>
                    <span style="font-size:0.88rem;color:#e2e8f0;">{step}</span>
                </div>""", unsafe_allow_html=True)


# ── EXAMS ──
def page_exams():
    page_header("📝 Placement Exams", "Test your knowledge with real placement-type questions")

    diff_tab = st.session_state.get('exam_diff', None)
    tabs = st.tabs(["🟢  Easy", "🟡  Medium", "🔴  Hard"])

    for tab_idx, (tab, difficulty) in enumerate(zip(tabs, ["Easy", "Medium", "Hard"])):
        with tab:
            if diff_tab == difficulty:
                st.session_state['exam_diff'] = None  # reset

            q_key   = f"exam_answers_{difficulty}"
            sub_key = f"exam_submitted_{difficulty}"
            score_key = f"exam_score_{difficulty}"

            questions = EXAM_QUESTIONS[difficulty]

            # Header banner
            colors = {"Easy": ("diff-easy","#10b981","🟢"), "Medium": ("diff-medium","#f59e0b","🟡"), "Hard": ("diff-hard","#ef4444","🔴")}
            cls, col, icon = colors[difficulty]
            st.markdown(f"""
            <div class="exam-difficulty-banner {cls}">
                <span style="font-size:2rem;">{icon}</span>
                <div>
                    <div style="font-weight:700;font-size:1rem;color:{col};">{difficulty} Level</div>
                    <div style="font-size:0.82rem;color:#94a3b8;">{len(questions)} Questions — Placement Aptitude & CS Fundamentals</div>
                </div>
                <div style="margin-left:auto;text-align:right;">
                    <div style="font-size:1.5rem;font-weight:800;color:{col};">{len(questions)}</div>
                    <div style="font-size:0.75rem;color:#94a3b8;">Questions</div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Already submitted → show results
            if st.session_state.get(sub_key):
                answers  = st.session_state.get(q_key, {})
                score_d  = st.session_state.get(score_key, {})
                correct  = score_d.get('correct', 0)
                total    = score_d.get('total', len(questions))
                pct      = int(correct / total * 100) if total else 0
                grade    = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"
                g_color  = "#10b981" if pct>=70 else "#f59e0b" if pct>=50 else "#ef4444"

                st.markdown(f"""
                <div class="result-banner">
                    <div style="font-size:0.9rem;color:#94a3b8;margin-bottom:8px;">Your Score</div>
                    <div class="result-score">{pct}%</div>
                    <div class="result-label">{correct} / {total} correct answers</div>
                    <div class="result-grade" style="color:{g_color};">Grade: {grade}</div>
                </div>""", unsafe_allow_html=True)

                # Score breakdown
                sc1, sc2, sc3 = st.columns(3)
                with sc1: metric_card("✅", correct,        "Correct",  "green")
                with sc2: metric_card("❌", total-correct,  "Wrong",    "pink")
                with sc3: metric_card("🏅", f"{pct}%",      "Score",    "purple")

                # Update user stats
                user_email = st.session_state.get('email','')
                user = get_current_user() or {}
                if user_email:
                    update_user(user_email, {
                        'exams_taken': user.get('exams_taken', 0) + 1,
                        'highest_score': max(user.get('highest_score', 0), pct),
                    })

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown("### 📋 Answer Review")

                for i, q in enumerate(questions):
                    user_ans = answers.get(i)
                    correct_ans = q['ans']
                    is_correct = user_ans == correct_ans

                    if is_correct:
                        status_html = '<span style="color:#10b981;font-weight:700;">✅ Correct!</span>'
                    elif user_ans is None:
                        status_html = '<span style="color:#f59e0b;font-weight:700;">⚠️ Not Answered</span>'
                    else:
                        status_html = '<span style="color:#ef4444;font-weight:700;">❌ Wrong</span>'

                    with st.expander(f"Q{i+1}: {q['q'][:70]}{'…' if len(q['q'])>70 else ''}  — {status_html}", expanded=False):
                        st.markdown(f"**Question:** {q['q']}")
                        if user_ans:
                            cls_ans = "ans-correct" if is_correct else "ans-wrong"
                            st.markdown(f'<div class="{cls_ans}">Your Answer: {user_ans}</div>', unsafe_allow_html=True)
                        if not is_correct:
                            st.markdown(f'<div class="ans-correct-reveal">✅ Correct Answer: {correct_ans}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="margin-top:8px;font-size:0.83rem;color:#94a3b8;background:#0f172a;padding:8px 12px;border-radius:8px;">💡 {q["exp"]}</div>', unsafe_allow_html=True)

                col_retry, _ = st.columns([1, 2])
                with col_retry:
                    if st.button(f"🔄 Retake {difficulty} Exam", key=f"retry_{difficulty}", use_container_width=True):
                        del st.session_state[sub_key]
                        if q_key in st.session_state: del st.session_state[q_key]
                        if score_key in st.session_state: del st.session_state[score_key]
                        st.rerun()

            else:
                # Show questions
                if q_key not in st.session_state:
                    st.session_state[q_key] = {}

                answers = st.session_state[q_key]

                with st.form(key=f"exam_form_{difficulty}"):
                    for i, q in enumerate(questions):
                        st.markdown(f"""
                        <div class="question-block">
                            <span class="question-number">Q {i+1}</span>
                            <div class="question-text">{q['q']}</div>
                        </div>""", unsafe_allow_html=True)

                        choice = st.radio(
                            f"Select answer for Q{i+1}",
                            q['opts'],
                            key=f"{difficulty}_q{i}",
                            index=None,
                            label_visibility="collapsed",
                        )
                        answers[i] = choice
                        st.markdown("<br>", unsafe_allow_html=True)

                    submitted = st.form_submit_button(f"Submit {difficulty} Exam ✔️", use_container_width=True)

                    if submitted:
                        correct = sum(1 for i, q in enumerate(questions) if answers.get(i) == q['ans'])
                        st.session_state[q_key]    = answers
                        st.session_state[sub_key]  = True
                        st.session_state[score_key] = {'correct': correct, 'total': len(questions)}
                        st.rerun()


# ── LEARNING RESOURCES ──
def page_learning():
    page_header("📚 Learning Resources", "Curated courses, tutorials and tools for your career")

    search = st.text_input("🔍 Search resources", placeholder="e.g. Python, Machine Learning, SQL…")

    categories = {
        "🐍 Python & Programming": [
            ("📺", "Python for Everybody",     "Coursera (University of Michigan) — Beginner friendly",  "https://www.coursera.org/specializations/python"),
            ("📺", "CS50 by Harvard",           "Free CS fundamentals course — Highly recommended",        "https://cs50.harvard.edu"),
            ("📖", "Real Python Tutorials",     "In-depth Python articles and exercises",                  "https://realpython.com"),
            ("🎮", "LeetCode",                  "Practice 2000+ coding problems for placements",           "https://leetcode.com"),
            ("🎮", "HackerRank",                "Skill-based coding challenges and certifications",        "https://hackerrank.com"),
        ],
        "🤖 Machine Learning & AI": [
            ("📺", "ML by Andrew Ng (Coursera)", "The gold standard ML course — Free to audit",            "https://coursera.org/learn/machine-learning"),
            ("📺", "Fast.ai Practical DL",       "Top-down deep learning for practitioners",               "https://fast.ai"),
            ("📖", "Kaggle Learn",               "Free micro-courses on ML, pandas, SQL, and more",        "https://kaggle.com/learn"),
            ("📺", "DeepLearning.AI Specialisation","5-course deep learning specialisation by Andrew Ng",  "https://deeplearning.ai"),
            ("📖", "Towards Data Science",       "Curated ML articles on Medium",                          "https://towardsdatascience.com"),
        ],
        "🌐 Web Development": [
            ("📖", "The Odin Project",           "Full-stack web dev curriculum — completely free",         "https://theodinproject.com"),
            ("📺", "freeCodeCamp",               "1400+ hours of web dev content — certifications",        "https://freecodecamp.org"),
            ("📖", "MDN Web Docs",               "Official reference for HTML, CSS, JavaScript",           "https://developer.mozilla.org"),
            ("🎮", "Frontend Mentor",            "Build real projects from professional designs",          "https://frontendmentor.io"),
            ("📺", "React Official Docs",         "Interactive tutorial and full documentation",            "https://react.dev"),
        ],
        "☁️ Cloud & DevOps": [
            ("📺", "AWS Training (Free)",        "Official AWS free training and certification prep",       "https://aws.training"),
            ("📖", "Docker Official Docs",       "Comprehensive Docker documentation and tutorials",       "https://docs.docker.com"),
            ("📺", "KodeKloud",                  "Hands-on DevOps labs for Docker, K8s, Ansible",         "https://kodekloud.com"),
            ("📖", "Linux Journey",              "Free interactive Linux learning platform",               "https://linuxjourney.com"),
            ("🎮", "Kubernetes Play",            "In-browser Kubernetes playground — no install needed",   "https://labs.play-with-k8s.com"),
        ],
        "💼 Placement Preparation": [
            ("🎮", "GeeksforGeeks",              "DSA, system design, company-wise interview questions",   "https://geeksforgeeks.org"),
            ("📺", "Apna College YouTube",       "Free DSA + placement prep in Hindi/English",             "https://youtube.com/@ApnaCollegeOfficial"),
            ("📖", "InterviewBit",               "Structured placement prep with mock interviews",         "https://interviewbit.com"),
            ("📖", "Glassdoor",                  "Real interview experiences from top companies",          "https://glassdoor.com"),
            ("🎮", "Codeforces",                 "Competitive programming for advanced preparation",       "https://codeforces.com"),
        ],
        "📊 Data Science Tools": [
            ("📖", "Pandas Documentation",       "Official pandas guide for data manipulation",            "https://pandas.pydata.org/docs"),
            ("📖", "Scikit-learn Docs",          "Official ML library guide with examples",                "https://scikit-learn.org"),
            ("📺", "Tableau Public",             "Free data visualisation tool with tutorials",            "https://public.tableau.com"),
            ("📖", "SQL Tutorial (W3Schools)",   "Interactive SQL practice for beginners",                 "https://w3schools.com/sql"),
            ("📖", "Kaggle Datasets",            "Free public datasets for practice projects",             "https://kaggle.com/datasets"),
        ],
    }

    icon_map = {"📺": "Video Course", "📖": "Documentation", "🎮": "Practice"}

    for cat, resources in categories.items():
        filtered = resources
        if search:
            filtered = [r for r in resources if search.lower() in r[1].lower() or search.lower() in r[2].lower()]
        if not filtered:
            continue
        st.markdown(f'<div class="section-title" style="margin-top:20px;">{cat}</div>', unsafe_allow_html=True)
        for icon, title, desc, link in filtered:
            st.markdown(f"""
            <div class="resource-card">
                <div class="resource-icon">{icon}</div>
                <div style="flex:1;">
                    <div class="resource-title">{title}</div>
                    <div class="resource-desc">{desc}</div>
                </div>
                <div>
                    <span class="badge badge-blue">{icon_map.get(icon,'Resource')}</span>
                    <br>
                    <a class="resource-link" href="{link}" target="_blank">Visit →</a>
                </div>
            </div>""", unsafe_allow_html=True)


# ── PROFILE ──
def page_profile():
    page_header("👤 My Profile", "View and update your career profile")

    user = get_current_user() or {}
    skills = st.session_state.get('extracted_skills') or user.get('skills', [])

    col_left, col_right = st.columns([2, 3])
    with col_left:
        st.markdown(f"""
        <div class="profile-header">
            <div class="profile-avatar">👨‍🎓</div>
            <div class="profile-name">{user.get('name', 'Student')}</div>
            <div class="profile-role">{user.get('domain','')}</div>
            <div style="margin-top:10px;">
                <span class="badge badge-purple">{user.get('year','Student')}</span>
                <span class="badge badge-blue" style="margin-left:6px;">{user.get('college','')}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card">
            <div class="section-title">📊 Progress Stats</div>
        </div>""", unsafe_allow_html=True)
        for icon, label, val, color in [
            ("📋","Resume Score",  f"{user.get('resume_score',0)}%",  "#7c3aed"),
            ("💼","Job Match",     f"{user.get('job_match',0)}%",     "#2563eb"),
            ("📝","Exams Taken",   user.get('exams_taken',0),          "#10b981"),
            ("🏆","Highest Score", f"{user.get('highest_score',0)}%", "#f59e0b"),
        ]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e293b;">
                <span style="font-size:0.85rem;color:#94a3b8;">{icon} {label}</span>
                <span style="font-size:0.95rem;font-weight:700;color:{color};">{val}</span>
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown("### ✏️ Edit Profile")
        with st.form("profile_form"):
            new_name   = st.text_input("Full Name",          value=user.get('name',''))
            new_college= st.text_input("College/University", value=user.get('college',''))
            new_domain = st.selectbox("Target Domain", [
                "Data Science", "Machine Learning", "Web Development",
                "Cloud & DevOps", "Mobile Development",
                "Cybersecurity", "Software Engineering", "UI/UX Design"],
                index=["Data Science","Machine Learning","Web Development","Cloud & DevOps",
                       "Mobile Development","Cybersecurity","Software Engineering","UI/UX Design"].index(
                    user.get('domain','Data Science')) if user.get('domain') in
                    ["Data Science","Machine Learning","Web Development","Cloud & DevOps",
                     "Mobile Development","Cybersecurity","Software Engineering","UI/UX Design"] else 0)
            new_year   = st.selectbox("Year of Study", ["1st Year","2nd Year","3rd Year","4th Year","Graduate"],
                                      index=["1st Year","2nd Year","3rd Year","4th Year","Graduate"].index(
                                          user.get('year','1st Year')) if user.get('year') in
                                          ["1st Year","2nd Year","3rd Year","4th Year","Graduate"] else 0)
            skills_text = st.text_area("Skills (comma separated)",
                                       value=", ".join(skills) if skills else "",
                                       placeholder="Python, Machine Learning, SQL…", height=80)
            save = st.form_submit_button("💾 Save Changes", use_container_width=True)
            if save:
                new_skills = [s.strip() for s in skills_text.split(',') if s.strip()]
                user_email = st.session_state.get('email','')
                if user_email:
                    update_user(user_email, {
                        'name': new_name, 'college': new_college,
                        'domain': new_domain, 'year': new_year, 'skills': new_skills,
                    })
                    st.session_state['extracted_skills'] = new_skills
                st.success("✅ Profile updated!")
                st.rerun()

        # Skills display
        if skills:
            st.markdown('<div class="section-title" style="margin-top:20px;">🔧 Current Skills</div>', unsafe_allow_html=True)
            st.markdown(skill_tags(skills), unsafe_allow_html=True)


# ── ABOUT ──
def page_about():
    page_header("ℹ️ About SmartHire", "AI-Powered Career Guidance Platform")

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        <div class="card">
            <div class="section-title">🎯 Our Mission</div>
            <p style="color:#94a3b8;font-size:0.9rem;line-height:1.7;">
                SmartHire is an AI-powered career guidance platform built to help students and fresh graduates
                navigate the job market intelligently. We use Machine Learning to analyse resumes, match jobs,
                identify skill gaps, and prepare students for placement interviews.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:16px;">
            <div class="section-title">⚙️ How It Works</div>
        </div>""", unsafe_allow_html=True)
        steps = [
            ("1","Upload Resume","We extract text, skills, education and experience using NLP parsing.","#7c3aed"),
            ("2","ML Analysis","TF-IDF vectorisation + classification predicts your best-fit domain.","#2563eb"),
            ("3","Job Matching","Cosine similarity matches your profile to 25+ job postings.","#10b981"),
            ("4","Skill Gap Report","We compare your skills vs. industry requirements for your target role.","#f59e0b"),
            ("5","Exam & Learn","Practice with placement-level questions and access curated resources.","#ec4899"),
        ]
        for num, title, desc, color in steps:
            st.markdown(f"""
            <div style="display:flex;gap:14px;padding:12px 0;border-bottom:1px solid #1e293b;align-items:flex-start;">
                <div style="background:{color};color:#fff;border-radius:50%;width:28px;height:28px;
                    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.8rem;flex-shrink:0;margin-top:2px;">
                    {num}
                </div>
                <div>
                    <div style="font-weight:600;color:#e2e8f0;margin-bottom:2px;">{title}</div>
                    <div style="font-size:0.82rem;color:#94a3b8;">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="card">
            <div class="section-title">🛠️ Tech Stack</div>
        </div>""", unsafe_allow_html=True)
        tech = [
            ("🐍","Python 3.11",    "Core language"),
            ("📊","Streamlit",       "Web framework"),
            ("🤖","Scikit-learn",    "ML models"),
            ("🔢","NumPy / Pandas",  "Data processing"),
            ("📖","PyPDF2 / docx",   "Resume parsing"),
            ("📈","Plotly",          "Visualisations"),
        ]
        for icon, name, desc in tech:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:center;padding:9px 0;border-bottom:1px solid #1e293b;">
                <span style="font-size:1.3rem;">{icon}</span>
                <div>
                    <div style="font-size:0.88rem;font-weight:600;color:#e2e8f0;">{name}</div>
                    <div style="font-size:0.75rem;color:#64748b;">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:16px;text-align:center;padding:24px;">
            <div style="font-size:2rem;">🎓</div>
            <div style="font-weight:700;color:#e2e8f0;margin:8px 0;">SmartHire v1.0</div>
            <div style="font-size:0.8rem;color:#64748b;">Machine Learning Industrial Project</div>
            <div style="font-size:0.78rem;color:#64748b;margin-top:6px;">© 2025 SmartHire. All rights reserved.</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────
def main():
    if not check_auth():
        show_login_page()
        return

    show_sidebar()

    # Route to page
    page = st.session_state.get('current_page', 'dashboard')
    PAGE_MAP = {
        'dashboard':      page_dashboard,
        'resume_upload':  page_resume_upload,
        'resume_analysis':page_resume_analysis,
        'jobs':           page_jobs,
        'skill_gap':      page_skill_gap,
        'exams':          page_exams,
        'learning':       page_learning,
        'profile':        page_profile,
        'about':          page_about,
    }
    render_fn = PAGE_MAP.get(page, page_dashboard)
    render_fn()


if __name__ == '__main__':
    main()
