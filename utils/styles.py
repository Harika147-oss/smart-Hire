def get_css():
    return """
<style>
/* ===== GLOBAL ===== */
* { box-sizing: border-box; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stSidebarNavItems"] { display: none !important; }
section[data-testid="stSidebarNav"] { display: none !important; }

.stApp {
    background: #0a0a1a;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12112A 0%, #1a0533 60%, #0d1b2a 100%) !important;
    border-right: 1px solid #2d2b55 !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ===== NAV BUTTONS ===== */
div[data-testid="stVerticalBlock"] > div > div > div > div.stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
div[data-testid="stVerticalBlock"] > div > div > div > div.stButton > button:hover {
    background: rgba(124,58,237,0.2) !important;
    color: #e2e8f0 !important;
    transform: none !important;
}

/* ===== MAIN CONTENT ===== */
.main-content {
    padding: 0;
}

/* ===== CARDS ===== */
.card {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(124,58,237,0.15);
}

/* ===== METRIC CARDS ===== */
.metric-card {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.metric-purple::before { background: linear-gradient(90deg,#7c3aed,#a855f7); }
.metric-blue::before   { background: linear-gradient(90deg,#2563eb,#3b82f6); }
.metric-green::before  { background: linear-gradient(90deg,#059669,#10b981); }
.metric-orange::before { background: linear-gradient(90deg,#d97706,#f59e0b); }
.metric-pink::before   { background: linear-gradient(90deg,#db2777,#ec4899); }
.metric-icon { font-size: 1.8rem; margin-bottom: 6px; display: block; }
.metric-value { font-size: 2rem; font-weight: 800; color: #fff; line-height: 1; }
.metric-label { font-size: 0.78rem; color: #94a3b8; margin-top: 5px; }

/* ===== PAGE HEADER ===== */
.page-header {
    background: linear-gradient(135deg,#1e1b4b 0%,#0f172a 100%);
    border: 1px solid #2d2b55;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 22px;
}
.page-header h1 { font-size: 1.7rem; font-weight: 700; color: #fff; margin: 0; }
.page-header p  { color: #94a3b8; margin: 5px 0 0; font-size: 0.9rem; }

/* ===== WELCOME BANNER ===== */
.welcome-banner {
    background: linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#1e3a5f 100%);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.welcome-banner::after {
    content: '';
    position: absolute;
    right: -30px; top: -30px;
    width: 200px; height: 200px;
    background: radial-gradient(circle,rgba(124,58,237,0.3) 0%,transparent 70%);
    border-radius: 50%;
}
.welcome-banner h1 { font-size: 1.9rem; font-weight: 800; color: #fff; margin-bottom: 8px; }
.welcome-banner p  { color: #c4b5fd; font-size: 0.95rem; max-width: 520px; }

/* ===== SECTION TITLE ===== */
.section-title {
    font-size: 1rem; font-weight: 600; color: #e2e8f0;
    margin: 18px 0 12px;
    display: flex; align-items: center; gap: 8px;
}

/* ===== BADGES ===== */
.badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 0.73rem; font-weight: 600; }
.badge-purple { background: rgba(124,58,237,0.2); color: #a78bfa; }
.badge-green  { background: rgba(16,185,129,0.2);  color: #34d399; }
.badge-blue   { background: rgba(37,99,235,0.2);   color: #60a5fa; }
.badge-orange { background: rgba(245,158,11,0.2);  color: #fbbf24; }
.badge-red    { background: rgba(239,68,68,0.2);   color: #f87171; }

/* ===== SKILL TAGS ===== */
.skill-tag {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa; border-radius: 8px;
    padding: 3px 11px; font-size: 0.78rem; margin: 3px;
}
.skill-tag-missing {
    display: inline-block;
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.3);
    color: #f87171; border-radius: 8px;
    padding: 3px 11px; font-size: 0.78rem; margin: 3px;
}

/* ===== JOB CARDS ===== */
.job-card {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.job-card:hover { border-color: #7c3aed; box-shadow: 0 4px 20px rgba(124,58,237,0.15); transform: translateY(-1px); }
.job-title   { font-size: 1rem; font-weight: 700; color: #fff; margin-bottom: 3px; }
.job-company { font-size: 0.84rem; color: #94a3b8; margin-bottom: 8px; }
.job-match   { display: inline-block; background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); border-radius: 999px; padding: 2px 10px; font-size: 0.73rem; font-weight: 700; }

/* ===== EXAM STYLES ===== */
.exam-difficulty-banner {
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 14px;
}
.diff-easy   { background: linear-gradient(135deg,rgba(16,185,129,0.15),rgba(5,150,105,0.1)); border: 1px solid rgba(16,185,129,0.3); }
.diff-medium { background: linear-gradient(135deg,rgba(245,158,11,0.15),rgba(217,119,6,0.1)); border: 1px solid rgba(245,158,11,0.3); }
.diff-hard   { background: linear-gradient(135deg,rgba(239,68,68,0.15),rgba(220,38,38,0.1)); border: 1px solid rgba(239,68,68,0.3); }

.question-block {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.question-number {
    display: inline-block;
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    color: #fff; border-radius: 7px;
    padding: 2px 10px; font-size: 0.75rem; font-weight: 700; margin-bottom: 8px;
}
.question-text { font-size: 0.97rem; font-weight: 600; color: #e2e8f0; line-height: 1.5; margin-bottom: 12px; }

.result-banner {
    background: linear-gradient(135deg,#1e1b4b,#1e3a5f);
    border: 1px solid #2d2b55;
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    margin-bottom: 24px;
}
.result-score {
    font-size: 4.5rem; font-weight: 900;
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1;
}
.result-label { font-size: 1.1rem; color: #94a3b8; margin-top: 8px; }
.result-grade { font-size: 1.4rem; font-weight: 700; margin: 12px 0 0; }

.ans-correct { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.4); border-radius: 8px; padding: 6px 12px; color: #34d399; margin: 3px 0; font-size: 0.85rem; }
.ans-wrong   { background: rgba(239,68,68,0.1);   border: 1px solid rgba(239,68,68,0.4);  border-radius: 8px; padding: 6px 12px; color: #f87171; margin: 3px 0; font-size: 0.85rem; }
.ans-correct-reveal { background: rgba(16,185,129,0.08); border-left: 3px solid #10b981; padding: 6px 12px; color: #6ee7b7; margin: 4px 0; font-size: 0.82rem; border-radius: 0 8px 8px 0; }

/* ===== RESOURCE CARDS ===== */
.resource-card {
    background: #16213e; border: 1px solid #2d2b55; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 10px;
    display: flex; align-items: flex-start; gap: 14px;
    transition: all 0.2s;
}
.resource-card:hover { border-color: #7c3aed; transform: translateX(4px); }
.resource-icon { font-size: 1.7rem; flex-shrink: 0; margin-top: 2px; }
.resource-title { font-weight: 600; color: #e2e8f0; margin-bottom: 2px; font-size: 0.95rem; }
.resource-desc  { font-size: 0.8rem; color: #94a3b8; }
.resource-link  { font-size: 0.78rem; color: #7c3aed; text-decoration: none; }

/* ===== PROFILE ===== */
.profile-header {
    background: linear-gradient(135deg,#1e1b4b,#1e3a5f);
    border: 1px solid #2d2b55; border-radius: 20px; padding: 30px;
    text-align: center; margin-bottom: 22px;
}
.profile-avatar { font-size: 4rem; margin-bottom: 10px; }
.profile-name { font-size: 1.6rem; font-weight: 800; color: #fff; }
.profile-role { font-size: 0.9rem; color: #94a3b8; margin-top: 4px; }

/* ===== LOGIN PAGE ===== */
.login-hero {
    text-align: center;
    padding: 20px 0 10px;
}
.login-hero-icon { font-size: 3.5rem; }
.login-hero h1 {
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.login-hero p { color: #94a3b8; font-size: 0.9rem; margin-top: 4px; }

.feature-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; color: #94a3b8; font-size: 0.88rem; }
.feature-item span:first-child { color: #10b981; font-size: 1rem; }

/* ===== INPUTS (global) ===== */
.stTextInput > div > div > input {
    background: #0f172a !important; border: 1px solid #2d2b55 !important;
    border-radius: 10px !important; color: #e2e8f0 !important; padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important; }

.stSelectbox > div > div {
    background: #0f172a !important; border: 1px solid #2d2b55 !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: #0f172a !important; border-radius: 12px !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 8px !important; color: #94a3b8 !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg,#7c3aed,#2563eb) !important; color: #fff !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] { background: #0f172a !important; border: 2px dashed #2d2b55 !important; border-radius: 12px !important; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a1a; }
::-webkit-scrollbar-thumb { background: #2d2b55; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7c3aed; }

/* ===== DIVIDER ===== */
.custom-divider { height: 1px; background: linear-gradient(90deg,transparent,#2d2b55,transparent); margin: 18px 0; }

/* gradient text */
.gradient-text {
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    font-weight: 800;
}

/* sidebar user card */
.sidebar-user {
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 12px; padding: 12px 14px; margin: 8px 0 4px;
    display: flex; align-items: center; gap: 10px;
}
.sidebar-user-avatar { font-size: 1.8rem; }
.sidebar-user-name { font-size: 0.85rem; font-weight: 600; color: #e2e8f0 !important; }
.sidebar-user-email { font-size: 0.72rem; color: #94a3b8 !important; }

.sidebar-logo { text-align:center; padding: 16px 10px 10px; border-bottom: 1px solid #2d2b55; margin-bottom: 8px; }
.sidebar-logo h2 { font-size: 1.4rem; font-weight: 900; background: linear-gradient(135deg,#7c3aed,#2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.sidebar-logo p { font-size: 0.72rem; color: #64748b !important; margin-top: 3px; }

.sidebar-section { font-size: 0.68rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #4b5563 !important; padding: 14px 14px 4px; }

/* ===== DASHBOARD NEW CARDS ===== */
.dash-card {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.dash-card-title {
    font-size: 0.83rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.04em;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.dash-metric-card {
    background: #16213e;
    border: 1px solid #2d2b55;
    border-radius: 14px;
    padding: 18px 14px;
    margin-bottom: 14px;
}

/* ===== SIDEBAR ACTIVE NAV ===== */
.sidebar-nav-item button {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    text-align: left !important;
    width: 100% !important;
    padding: 9px 14px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.sidebar-nav-item button:hover {
    background: rgba(124,58,237,0.15) !important;
    color: #e2e8f0 !important;
}
.sidebar-nav-active button {
    background: linear-gradient(135deg,rgba(37,99,235,0.35),rgba(124,58,237,0.35)) !important;
    color: #fff !important;
    border-left: 3px solid #7c3aed !important;
}
</style>
"""