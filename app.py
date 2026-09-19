"""
app.py  -  Supermarket Sales Intelligence Platform
Run:  streamlit run app.py
"""

import os, sys, subprocess
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── paths ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.join(BASE_DIR, "src")
CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "supermarket_sales.csv")
PDF_PATH = os.path.join(BASE_DIR, "SUPER MARKET DATA.pdf")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from analysis import (
    load_data, total_sales, total_transactions, avg_sales_per_transaction,
    avg_rating, sales_by_branch, sales_by_category, sales_by_product,
    sales_by_payment, sales_by_customer_type, sales_by_gender,
    rating_by_category, rating_by_branch, monthly_sales, top_products,
    transactions_by_payment, verify_against_manual,
)

# ── page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS — Premium Dark BI Theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root / Body ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif !important;
}
.stApp {
    background-color: #0B1220 !important;
}
.block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0D1626 !important;
    border-right: 1px solid #1E293B !important;
    width: 240px !important;
    min-width: 240px !important;
}
section[data-testid="stSidebar"] > div {
    background: #0D1626 !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] * {
    color: #CBD5E1 !important;
}
section[data-testid="stSidebar"] .stMarkdown hr {
    border-color: #1E293B !important;
    margin: 8px 0 !important;
}

/* Sidebar multiselect / selectbox */
section[data-testid="stSidebar"] label p {
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: #151F32 !important;
    border-color: #1E293B !important;
}
section[data-testid="stSidebar"] .stDateInput input {
    background: #151F32 !important;
    border-color: #1E293B !important;
    color: #CBD5E1 !important;
    font-size: 12px !important;
}
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #64748B !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    text-align: left !important;
    padding: 8px 14px !important;
    width: 100% !important;
    justify-content: flex-start !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: #151F32 !important;
    border-color: #1E293B !important;
    color: #E2E8F0 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:focus:not(:active) {
    background: #162035 !important;
    border-color: #1E3A5F !important;
    color: #60A5FA !important;
    box-shadow: none !important;
    outline: none !important;
}

/* ── Navigation items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    color: #94A3B8;
    margin: 2px 0;
    transition: background 0.15s;
    border: 1px solid transparent;
}
.nav-item:hover { background: #151F32; color: #E2E8F0; }
.nav-item.active {
    background: #162035;
    color: #3B82F6;
    border-color: #1E3A5F;
    font-weight: 600;
}
.nav-icon { font-size: 14px; width: 18px; text-align: center; }

/* ── Main content area ── */
.main-header {
    background: linear-gradient(135deg, #0D1626 0%, #111827 50%, #0B1220 100%);
    border-bottom: 1px solid #1E293B;
    padding: 20px 32px 16px 32px;
    margin: -1px -2rem 24px -2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-left .title {
    font-size: 22px;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.3px;
    margin: 0;
    line-height: 1.2;
}
.header-left .subtitle {
    font-size: 12px;
    color: #64748B;
    margin-top: 3px;
    letter-spacing: 0.3px;
}
.header-left .desc {
    font-size: 11px;
    color: #475569;
    margin-top: 2px;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 8px;
}
.live-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #0F2017;
    border: 1px solid #166534;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: 700;
    color: #4ADE80;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.live-dot {
    width: 7px; height: 7px;
    background: #4ADE80;
    border-radius: 50%;
}

/* ── Section titles ── */
.sec-head {
    font-size: 14px;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: 0.3px;
    margin: 0 0 4px 0;
}
.sec-sub {
    font-size: 11px;
    color: #475569;
    margin: 0 0 16px 0;
}
.sec-divider {
    border: none;
    border-top: 1px solid #1E293B;
    margin: 20px 0;
}

/* ── KPI Cards ── */
.kpi-grid { display: flex; gap: 14px; margin-bottom: 20px; flex-wrap: wrap; }
.kpi-card {
    flex: 1;
    min-width: 140px;
    background: #151F32;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 16px 18px 14px 18px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #3B82F6);
}
.kpi-card.green::before  { background: #10B981; }
.kpi-card.amber::before  { background: #F59E0B; }
.kpi-card.purple::before { background: #8B5CF6; }
.kpi-card.teal::before   { background: #14B8A6; }
.kpi-card.rose::before   { background: #F43F5E; }

.kpi-icon  { font-size: 18px; margin-bottom: 8px; display: block; }
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #475569;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: #F1F5F9;
    line-height: 1.1;
    letter-spacing: -0.5px;
}
.kpi-value.sm { font-size: 18px; }
.kpi-support {
    font-size: 11px;
    color: #64748B;
    margin-top: 4px;
}

/* ── Chart Cards ── */
.chart-card {
    background: #151F32;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 20px 20px 10px 20px;
    margin-bottom: 16px;
}
.chart-title {
    font-size: 13px;
    font-weight: 700;
    color: #E2E8F0;
    margin: 0 0 2px 0;
}
.chart-subtitle {
    font-size: 11px;
    color: #475569;
    margin: 0 0 14px 0;
}

/* ── Data table ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #1E293B !important;
}
div[data-testid="stDataFrame"] table {
    background: #151F32 !important;
}
div[data-testid="stDataFrame"] th {
    background: #0D1626 !important;
    color: #64748B !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    border-bottom: 1px solid #1E293B !important;
}
div[data-testid="stDataFrame"] td {
    color: #CBD5E1 !important;
    font-size: 13px !important;
    border-bottom: 1px solid #162035 !important;
}

/* ── Alerts / Insights ── */
div[data-testid="stAlert"] {
    background: #151F32 !important;
    border-radius: 8px !important;
    border-left-width: 3px !important;
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #64748B !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border-radius: 0 !important;
    letter-spacing: 0.3px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #3B82F6 !important;
    border-bottom: 2px solid #3B82F6 !important;
}
div[data-testid="stTabs"] {
    border-bottom: 1px solid #1E293B;
    margin-bottom: 20px;
}

/* ── Expander ── */
details[data-testid="stExpander"] {
    background: #151F32 !important;
    border: 1px solid #1E293B !important;
    border-radius: 10px !important;
}
details[data-testid="stExpander"] summary {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* ── Status badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.badge-green  { background: #0F2017; color: #4ADE80; border: 1px solid #166534; }
.badge-red    { background: #1F0B0B; color: #F87171; border: 1px solid #7F1D1D; }
.badge-amber  { background: #1F1605; color: #FBB040; border: 1px solid #78350F; }
.badge-blue   { background: #0C1A2E; color: #60A5FA; border: 1px solid #1E3A5F; }

/* ── Insight cards ── */
.insight-card {
    background: #151F32;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.insight-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.insight-icon { font-size: 16px; }
.insight-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748B;
}
.insight-body {
    font-size: 13px;
    color: #CBD5E1;
    line-height: 1.6;
}
.insight-body strong { color: #F1F5F9; }

/* ── Validation cards ── */
.val-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.val-card {
    flex: 1;
    min-width: 160px;
    background: #151F32;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.val-card-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #475569;
    margin-bottom: 6px;
}
.val-card-value {
    font-size: 22px;
    font-weight: 800;
    color: #F1F5F9;
    margin-bottom: 4px;
}
.val-card-status { font-size: 11px; }

/* ── Footer ── */
.dashboard-footer {
    border-top: 1px solid #1E293B;
    padding: 14px 0 8px 0;
    text-align: center;
    font-size: 11px;
    color: #334155;
    margin-top: 32px;
}

/* ── Verification table ── */
.verify-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    border-radius: 10px;
    overflow: hidden;
}
.verify-table th {
    background: #0D1626;
    color: #475569;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 10px 14px;
    border-bottom: 1px solid #1E293B;
    text-align: left;
}
.verify-table td {
    padding: 11px 14px;
    color: #CBD5E1;
    border-bottom: 1px solid #162035;
    background: #151F32;
}
.verify-table tr:hover td { background: #182438; }
.verify-match   { color: #4ADE80; font-weight: 700; }
.verify-diff    { color: #FBB040; font-weight: 700; }

/* Override Streamlit metric widget */
div[data-testid="stMetric"] { display: none !important; }

/* Empty state */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #475569;
}
.empty-state-icon { font-size: 40px; margin-bottom: 12px; }
.empty-state-title { font-size: 16px; font-weight: 600; color: #64748B; margin-bottom: 6px; }
.empty-state-sub   { font-size: 13px; color: #475569; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def get_data():
    if not os.path.exists(CSV_PATH):
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError(f"PDF not found: {PDF_PATH}")
        r = subprocess.run(
            [sys.executable, os.path.join(SRC_DIR, "extract_data.py")],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
    return load_data(CSV_PATH)

try:
    df_full = get_data()
except Exception as e:
    st.markdown(f"""
    <div style="background:#1F0B0B;border:1px solid #7F1D1D;border-radius:10px;padding:24px;margin:40px auto;max-width:600px;text-align:center;">
        <div style="font-size:28px;margin-bottom:12px;">⚠️</div>
        <div style="font-size:16px;font-weight:700;color:#F87171;margin-bottom:8px;">Unable to Load Dataset</div>
        <div style="font-size:13px;color:#FCA5A5;">Please verify the dataset file exists and is accessible.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════
# SIDEBAR — Navigation + Filters
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 12px 16px; border-bottom:1px solid #1E293B; margin-bottom:12px;">
        <div style="font-size:18px; font-weight:800; color:#F1F5F9; letter-spacing:-0.3px;">📊 SUPERMARKET</div>
        <div style="font-size:9px; font-weight:700; letter-spacing:2px; color:#3B82F6; margin-top:2px; text-transform:uppercase;">Sales Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    pages = [
        ("overview",   "◼",  "Overview"),
        ("sales",      "📈", "Sales Analysis"),
        ("branch",     "🏪", "Branch Performance"),
        ("product",    "📦", "Product & Category"),
        ("customer",   "👥", "Customer Analysis"),
        ("payment",    "💳", "Payment Analysis"),
        ("ratings",    "⭐", "Ratings"),
        ("quality",    "✅", "Data Quality"),
    ]

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    st.markdown('<div style="font-size:9px;font-weight:700;letter-spacing:1.5px;color:#334155;text-transform:uppercase;padding:0 6px 6px 6px;">NAVIGATION</div>', unsafe_allow_html=True)
    for pid, icon, label in pages:
        active = "active" if st.session_state.page == pid else ""
        if st.button(f"{icon}  {label}", key=f"nav_{pid}",
                     use_container_width=True,
                     type="secondary"):
            st.session_state.page = pid
            st.rerun()

    st.markdown('<hr style="border-color:#1E293B;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:9px;font-weight:700;letter-spacing:1.5px;color:#334155;text-transform:uppercase;padding:0 6px 6px 6px;">GLOBAL FILTERS</div>', unsafe_allow_html=True)

    branches   = sorted(df_full["Branch"].unique())
    cities     = sorted(df_full["City"].unique())
    categories = sorted(df_full["Category"].unique())
    products   = sorted(df_full["Product"].unique())
    cust_types = sorted(df_full["Customer Type"].unique())
    genders    = sorted(df_full["Gender"].unique())
    payments   = sorted(df_full["Payment"].unique())

    sel_branch    = st.multiselect("Branch",          branches,   default=branches,   format_func=lambda b: f"Branch {b}")
    sel_city      = st.multiselect("City",            cities,     default=cities)
    sel_category  = st.multiselect("Category",        categories, default=categories)
    sel_cust_type = st.multiselect("Customer Type",   cust_types, default=cust_types)
    sel_gender    = st.multiselect("Gender",          genders,    default=genders)
    sel_payment   = st.multiselect("Payment Method",  payments,   default=payments)

    date_min = df_full["Date"].min().date()
    date_max = df_full["Date"].max().date()
    sel_dates = st.date_input("Date Range",
                               value=(date_min, date_max),
                               min_value=date_min,
                               max_value=date_max)

    if st.button("↺  Reset All Filters", use_container_width=True, type="secondary"):
        st.session_state.page = st.session_state.page
        for k in ["sel_branch","sel_city","sel_category","sel_cust_type","sel_gender","sel_payment"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown('<hr style="border-color:#1E293B;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:11px;color:#334155;text-align:center;">'
        f'Dataset: <span style="color:#64748B;font-weight:600;">{len(df_full):,} transactions</span></div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# APPLY FILTERS
# ══════════════════════════════════════════════════════════════
mask = (
    df_full["Branch"].isin(sel_branch) &
    df_full["City"].isin(sel_city) &
    df_full["Category"].isin(sel_category) &
    df_full["Customer Type"].isin(sel_cust_type) &
    df_full["Gender"].isin(sel_gender) &
    df_full["Payment"].isin(sel_payment)
)
if len(sel_dates) == 2:
    mask &= (
        (df_full["Date"].dt.date >= sel_dates[0]) &
        (df_full["Date"].dt.date <= sel_dates[1])
    )
df = df_full[mask].copy()

# ══════════════════════════════════════════════════════════════
# GLOBAL PLOTLY THEME
# ══════════════════════════════════════════════════════════════
PLOT_BG     = "#151F32"
PAPER_BG    = "#151F32"
GRID_COLOR  = "#1E293B"
TEXT_COLOR  = "#94A3B8"
FONT_FAMILY = "Inter, -apple-system, Segoe UI, sans-serif"

BRANCH_COLORS  = {"A": "#3B82F6", "B": "#10B981", "C": "#F59E0B", "D": "#EF4444"}
CATEGORY_PAL   = ["#3B82F6","#10B981","#F59E0B","#8B5CF6","#F43F5E","#14B8A6","#FB923C","#A3E635"]
PAYMENT_COLORS = {"UPI": "#3B82F6", "Card": "#10B981", "Cash": "#F59E0B", "Net Banking": "#8B5CF6"}

def apply_chart_theme(fig, height=320, show_legend=True):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=12),
        height=height,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#1E293B",
            font=dict(size=11, color="#94A3B8"),
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR, gridwidth=1,
            linecolor="#1E293B",
            tickfont=dict(size=11, color="#64748B"),
            title_font=dict(size=11, color="#64748B"),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, gridwidth=1,
            linecolor="#1E293B",
            tickfont=dict(size=11, color="#64748B"),
            title_font=dict(size=11, color="#64748B"),
        ),
    )
    return fig

def chart_card(title, subtitle=""):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-title">{title}</div>
        <div class="chart-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)

def chart_card_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="main-header">
    <div class="header-left">
        <div class="title">SUPERMARKET SALES INTELLIGENCE</div>
        <div class="subtitle">Interactive Business Analytics Dashboard</div>
        <div class="desc">Explore sales performance, customer behavior, product trends, payment patterns and branch insights.</div>
    </div>
    <div class="header-right">
        <div class="live-badge">
            <div class="live-dot"></div>
            LIVE ANALYTICS
        </div>
        <div style="font-size:11px;color:#334155;text-align:right;margin-left:12px;">
            {df_full['Date'].min().strftime('%b %Y')} – {df_full['Date'].max().strftime('%b %Y')}<br>
            <span style="color:#3B82F6;font-weight:700;">{len(df):,}</span> / {len(df_full):,} records
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# EMPTY STATE
# ══════════════════════════════════════════════════════════════
if df.empty:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-title">No Data for Selected Filters</div>
        <div class="empty-state-sub">Adjust the sidebar filters or reset to view all data.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════
# HELPER: KPI card HTML
# ══════════════════════════════════════════════════════════════
def kpi_card(icon, label, value, support="", accent=""):
    acc_cls = f" {accent}" if accent else ""
    return f"""
    <div class="kpi-card{acc_cls}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value{'  sm' if len(str(value)) > 12 else ''}">{value}</div>
        <div class="kpi-support">{support}</div>
    </div>"""

def kpi_row(cards_html):
    st.markdown(f'<div class="kpi-grid">{"".join(cards_html)}</div>', unsafe_allow_html=True)

def section_header(title, subtitle=""):
    st.markdown(f'<div class="sec-head">{title}</div><div class="sec-sub">{subtitle}</div>', unsafe_allow_html=True)

def insight_card(icon, title, body):
    return f"""
    <div class="insight-card">
        <div class="insight-header">
            <span class="insight-icon">{icon}</span>
            <span class="insight-title">{title}</span>
        </div>
        <div class="insight-body">{body}</div>
    </div>"""

# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "overview":
    ts     = total_sales(df)
    tx     = total_transactions(df)
    avg_tx = avg_sales_per_transaction(df)
    rat    = avg_rating(df)
    bdf    = sales_by_branch(df)
    catdf  = sales_by_category(df)
    prd    = top_products(df, 1)
    best_b = bdf.iloc[0]
    best_c = catdf.iloc[0]
    best_p = prd.iloc[0] if not prd.empty else None

    # ── KPI row ──
    cards = [
        kpi_card("💰", "Total Sales", f"₹{ts:,.0f}", "Overall revenue"),
        kpi_card("🧾", "Transactions", f"{tx:,}", "Total invoices", "green"),
        kpi_card("📊", "Avg. Transaction", f"₹{avg_tx:,.2f}", "Per invoice", "amber"),
        kpi_card("⭐", "Avg. Rating", f"{rat} / 5", "Customer satisfaction", "purple"),
        kpi_card("🏪", "Top Branch", f"Branch {best_b['Branch']}", best_b["City"], "teal"),
        kpi_card("🏷️", "Top Category", best_c["Category"], f"₹{best_c['Total Sales']:,.0f}", "rose"),
    ]
    if best_p is not None:
        cards.append(kpi_card("📦", "Top Product", best_p["Product"], f"₹{best_p['Total Sales']:,.0f}"))
    kpi_row(cards)

    # ── Sales Trend + Category pie ──
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Sales Performance Over Time</div>
            <div class="chart-subtitle">Track revenue movement across the selected period</div>
        """, unsafe_allow_html=True)
        mon = monthly_sales(df)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mon["Month"], y=mon["Total Sales"],
            name="Monthly Sales",
            marker_color="#1E3A5F",
            hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=mon["Month"], y=mon["Total Sales"],
            mode="lines+markers",
            name="Trend",
            line=dict(color="#3B82F6", width=2.5),
            marker=dict(size=7, color="#3B82F6", line=dict(color="#0B1220", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300)
        fig.update_layout(xaxis_tickangle=-30, bargap=0.3)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Sales by Category</div>
            <div class="chart-subtitle">Contribution per category</div>
        """, unsafe_allow_html=True)
        fig = px.pie(catdf, names="Category", values="Total Sales",
                     color_discrete_sequence=CATEGORY_PAL, hole=0.5)
        fig.update_traces(
            textposition="inside", textinfo="percent+label",
            textfont=dict(size=11, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        )
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Branch + Category bars ──
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Branch Performance</div>
            <div class="chart-subtitle">Total sales ranked by branch</div>
        """, unsafe_allow_html=True)
        bdf2 = bdf.copy()
        bdf2["Label"] = bdf2.apply(lambda r: f"Branch {r['Branch']} ({r['City']})", axis=1)
        colors = [BRANCH_COLORS.get(b, "#3B82F6") for b in bdf2["Branch"]]
        fig = go.Figure(go.Bar(
            x=bdf2["Label"], y=bdf2["Total Sales"],
            marker_color=colors,
            text=[f"₹{v:,.0f}" for v in bdf2["Total Sales"]],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        fig.update_layout(yaxis_tickformat="₹,.0f")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Category Sales Ranking</div>
            <div class="chart-subtitle">Horizontal comparison by category</div>
        """, unsafe_allow_html=True)
        catdf_s = catdf.sort_values("Total Sales")
        fig = go.Figure(go.Bar(
            y=catdf_s["Category"], x=catdf_s["Total Sales"],
            orientation="h",
            marker_color=CATEGORY_PAL[:len(catdf_s)],
            text=[f"₹{v:,.0f}" for v in catdf_s["Total Sales"]],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Sales: ₹%{x:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Top Products + Payment donut ──
    col5, col6 = st.columns([3, 2])
    with col5:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Top 10 Products by Sales</div>
            <div class="chart-subtitle">Highest-revenue product ranking</div>
        """, unsafe_allow_html=True)
        tp10 = top_products(df, 10).sort_values("Total Sales")
        fig = go.Figure(go.Bar(
            y=tp10["Product"], x=tp10["Total Sales"],
            orientation="h",
            marker=dict(
                color=tp10["Total Sales"],
                colorscale=[[0, "#1E3A5F"], [1, "#3B82F6"]],
            ),
            text=[f"₹{v:,.0f}" for v in tp10["Total Sales"]],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Sales: ₹%{x:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=340, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Payment Method Distribution</div>
            <div class="chart-subtitle">Transaction share by payment</div>
        """, unsafe_allow_html=True)
        paydf = sales_by_payment(df)
        pay_colors = [PAYMENT_COLORS.get(p, "#3B82F6") for p in paydf["Payment"]]
        fig = go.Figure(go.Pie(
            labels=paydf["Payment"], values=paydf["Transactions"],
            hole=0.55,
            marker=dict(colors=pay_colors, line=dict(color="#0B1220", width=2)),
            textfont=dict(size=11, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>%{value} transactions (%{percent})<extra></extra>",
        ))
        apply_chart_theme(fig, height=340, show_legend=True)
        fig.update_layout(
            legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=11)),
            annotations=[dict(
                text=f"<b>{paydf.iloc[0]['Payment']}</b><br>Top",
                x=0.5, y=0.5, font=dict(size=12, color="#F1F5F9"), showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Business Insights ──
    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
    section_header("Business Insights", "Auto-generated from calculated data")

    ct    = sales_by_customer_type(df).set_index("Customer Type")
    m_av  = ct.loc["Member", "Avg_Transaction"] if "Member" in ct.index else 0
    n_av  = ct.loc["Normal", "Avg_Transaction"] if "Normal" in ct.index else 0
    bot_b = bdf.iloc[-1]
    top_pay = paydf.iloc[0]
    worst_cat = catdf.iloc[-1]

    ins_html  = insight_card("🏆", "Top Performer",
        f"<strong>Branch {best_b['Branch']} ({best_b['City']})</strong> leads with <strong>₹{best_b['Total Sales']:,.0f}</strong> in total sales — "
        f"{(best_b['Total Sales']/ts*100):.1f}% of all revenue.")
    ins_html += insight_card("📈", "Sales Opportunity",
        f"<strong>{best_c['Category']}</strong> is the highest-grossing category at <strong>₹{best_c['Total Sales']:,.0f}</strong> "
        f"({best_c['Total Sales']/ts*100:.1f}% of total sales).")
    ins_html += insight_card("👥", "Customer Behavior",
        f"{'<strong>Normal</strong> customers spend more per transaction (₹' + f'{n_av:,.2f}' + ') vs Members (₹' + f'{m_av:,.2f}' + ').'
          if n_av > m_av else
          '<strong>Members</strong> spend more per transaction (₹' + f'{m_av:,.2f}' + ') vs Normal (₹' + f'{n_av:,.2f}' + ').'} "
        f"This is driven by {df[df['Customer Type']==('Normal' if n_av>m_av else 'Member')].shape[0]:,} transactions.")
    ins_html += insight_card("💳", "Payment Trend",
        f"<strong>{top_pay['Payment']}</strong> dominates with <strong>{int(top_pay['Transactions'])}</strong> transactions "
        f"({top_pay['Transactions']/tx*100:.1f}% of total), generating ₹{top_pay['Total_Sales']:,.0f} in sales.")
    ins_html += insight_card("⭐", "Customer Experience",
        f"Overall average rating is <strong>{rat}/5.0</strong>. "
        f"{'Customers are broadly satisfied. Maintaining service quality is key.' if rat >= 4.0 else 'Rating is below 4.0 — targeted service improvements are recommended.'}")
    ins_html += insight_card("⚠️", "Area to Improve",
        f"<strong>Branch {bot_b['Branch']} ({bot_b['City']})</strong> has the lowest sales at <strong>₹{bot_b['Total Sales']:,.0f}</strong> "
        f"({bot_b['Total Sales']/ts*100:.1f}% of total). Also, <strong>{worst_cat['Category']}</strong> "
        f"is the weakest category at ₹{worst_cat['Total Sales']:,.0f}.")

    c_ins1, c_ins2 = st.columns(2)
    ins_list = ins_html.split('</div>\n    </div>')[:-1]
    for i, card in enumerate(ins_html.split('<div class="insight-card">')):
        if not card.strip():
            continue
        full = '<div class="insight-card">' + card
        (c_ins1 if i % 2 == 1 else c_ins2).markdown(full, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — SALES ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "sales":
    ts     = total_sales(df)
    tx     = total_transactions(df)
    avg_tx = avg_sales_per_transaction(df)
    mon    = monthly_sales(df)
    bdf    = sales_by_branch(df)
    catdf  = sales_by_category(df)

    cards = [
        kpi_card("💰", "Total Sales",       f"₹{ts:,.0f}",    "Filtered period"),
        kpi_card("🧾", "Transactions",       f"{tx:,}",        "Total invoices", "green"),
        kpi_card("📊", "Avg. Transaction",   f"₹{avg_tx:,.2f}","Per invoice",    "amber"),
        kpi_card("📅", "Months Covered",     f"{len(mon)}",    "Time periods",   "purple"),
    ]
    kpi_row(cards)

    # Sales Trend — full width
    section_header("Sales Trend Over Time", "Monthly revenue performance across the selected period")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=mon["Month"], y=mon["Total Sales"],
        name="Monthly Sales",
        marker_color="#182438",
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=mon["Month"], y=mon["Total Sales"],
        fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
        mode="lines+markers",
        line=dict(color="#3B82F6", width=2.5),
        marker=dict(size=8, color="#3B82F6", line=dict(color="#0B1220", width=2)),
        name="Trend Line",
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    apply_chart_theme(fig, height=340)
    fig.update_layout(xaxis_tickangle=-30, bargap=0.4, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        section_header("Sales by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        bdf2 = bdf.copy()
        bdf2["Label"] = bdf2.apply(lambda r: f"Branch {r['Branch']}\n({r['City']})", axis=1)
        colors = [BRANCH_COLORS.get(b, "#3B82F6") for b in bdf2["Branch"]]
        fig = go.Figure(go.Bar(
            x=bdf2["Label"], y=bdf2["Total Sales"],
            marker_color=colors,
            text=[f"₹{v:,.0f}" for v in bdf2["Total Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Sales by Category")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        catdf_s = catdf.sort_values("Total Sales")
        fig = go.Figure(go.Bar(
            y=catdf_s["Category"], x=catdf_s["Total Sales"],
            orientation="h",
            marker_color=CATEGORY_PAL[:len(catdf_s)],
            text=[f"₹{v:,.0f}" for v in catdf_s["Total Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Monthly summary table
    section_header("Monthly Performance Table")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    mon_disp = mon.copy()
    mon_disp["Total Sales"] = mon_disp["Total Sales"].apply(lambda v: f"₹{v:,.2f}")
    st.dataframe(mon_disp, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — BRANCH PERFORMANCE
# ══════════════════════════════════════════════════════════════
elif page == "branch":
    bdf = sales_by_branch(df)
    bdf["Label"] = bdf.apply(lambda r: f"Branch {r['Branch']} ({r['City']})", axis=1)

    # Branch KPI cards
    cards = []
    for _, row in bdf.iterrows():
        tx_cnt = df[df["Branch"] == row["Branch"]].shape[0]
        avg_tx = row["Total Sales"] / tx_cnt if tx_cnt > 0 else 0
        acc = {"A": "", "B": "green", "C": "amber", "D": "rose"}.get(row["Branch"], "")
        cards.append(kpi_card(
            "🏪", f"Branch {row['Branch']} — {row['City']}",
            f"₹{row['Total Sales']:,.0f}",
            f"{tx_cnt} txns · Avg ₹{avg_tx:,.0f}", acc
        ))
    kpi_row(cards)

    col1, col2 = st.columns(2)
    with col1:
        section_header("Total Sales by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        colors = [BRANCH_COLORS.get(b, "#3B82F6") for b in bdf["Branch"]]
        fig = go.Figure(go.Bar(
            x=bdf["Label"], y=bdf["Total Sales"],
            marker_color=colors,
            text=[f"₹{v:,.0f}" for v in bdf["Total Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Sales Share by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=bdf["Label"], values=bdf["Total Sales"],
            hole=0.5,
            marker=dict(colors=colors, line=dict(color="#0B1220", width=2)),
            textfont=dict(size=11, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        section_header("Transactions by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        tx_b = df.groupby(["Branch", "City"]).size().reset_index(name="Transactions")
        tx_b["Label"] = tx_b.apply(lambda r: f"Branch {r['Branch']} ({r['City']})", axis=1)
        colors2 = [BRANCH_COLORS.get(b, "#3B82F6") for b in tx_b["Branch"]]
        fig = go.Figure(go.Bar(
            x=tx_b["Label"], y=tx_b["Transactions"],
            marker_color=colors2,
            text=tx_b["Transactions"], textposition="outside",
            textfont=dict(size=11, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>%{y} transactions<extra></extra>",
        ))
        apply_chart_theme(fig, height=280, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        section_header("Avg. Transaction by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        avg_b = df.groupby(["Branch", "City"])["Sales"].mean().round(2).reset_index()
        avg_b["Label"] = avg_b.apply(lambda r: f"Branch {r['Branch']} ({r['City']})", axis=1)
        colors3 = [BRANCH_COLORS.get(b, "#3B82F6") for b in avg_b["Branch"]]
        fig = go.Figure(go.Bar(
            x=avg_b["Label"], y=avg_b["Sales"],
            marker_color=colors3,
            text=[f"₹{v:,.2f}" for v in avg_b["Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Avg ₹%{y:,.2f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=280, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("Category vs Branch Heatmap", "Sales intensity across branches and categories")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pvt = df.groupby(["Branch", "Category"])["Sales"].sum().unstack(fill_value=0).round(0)
    fig = px.imshow(pvt, color_continuous_scale=[[0,"#0D1626"],[0.5,"#1E3A5F"],[1,"#3B82F6"]],
                    text_auto=".0f", aspect="auto",
                    labels={"x": "Category", "y": "Branch", "color": "Sales"})
    apply_chart_theme(fig, height=260, show_legend=False)
    fig.update_traces(textfont=dict(size=10, color="#F1F5F9"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Branch Summary Table")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bsum = bdf[["Branch", "City", "Total Sales"]].copy()
    bsum["Transactions"] = [df[df["Branch"] == b].shape[0] for b in bsum["Branch"]]
    bsum["Avg / Tx"] = (bsum["Total Sales"] / bsum["Transactions"]).round(2)
    bsum["Avg Rating"] = [df[df["Branch"] == b]["Rating"].mean().round(2) for b in bsum["Branch"]]
    bsum["Total Sales"] = bsum["Total Sales"].apply(lambda v: f"₹{v:,.2f}")
    bsum["Avg / Tx"]   = bsum["Avg / Tx"].apply(lambda v: f"₹{v:,.2f}")
    st.dataframe(bsum.reset_index(drop=True), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — PRODUCT & CATEGORY
# ══════════════════════════════════════════════════════════════
elif page == "product":
    catdf = sales_by_category(df)
    tp    = top_products(df, 10)
    best_p = tp.iloc[0] if not tp.empty else None

    cards = [
        kpi_card("📦", "Top Product",   best_p["Product"] if best_p is not None else "N/A",
                 f"₹{best_p['Total Sales']:,.0f}" if best_p is not None else "", "green"),
        kpi_card("🏷️", "Top Category", catdf.iloc[0]["Category"], f"₹{catdf.iloc[0]['Total Sales']:,.0f}", "amber"),
        kpi_card("📊", "Categories",    f"{len(catdf)}", "Unique categories", "purple"),
        kpi_card("📦", "Products",      f"{df['Product'].nunique()}", "Unique products", "teal"),
    ]
    kpi_row(cards)

    col1, col2 = st.columns([3, 2])
    with col1:
        section_header("Top 10 Products by Sales", "Highest-revenue product ranking")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        tp_s = tp.sort_values("Total Sales")
        cat_color_map = {c: CATEGORY_PAL[i % len(CATEGORY_PAL)] for i, c in enumerate(df["Category"].unique())}
        bar_colors = [cat_color_map.get(c, "#3B82F6") for c in tp_s["Category"]]
        fig = go.Figure(go.Bar(
            y=tp_s["Product"], x=tp_s["Total Sales"],
            orientation="h",
            marker_color=bar_colors,
            text=[f"₹{v:,.0f}" for v in tp_s["Total Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=440, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Category Contribution")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=catdf["Category"], values=catdf["Total Sales"],
            hole=0.5,
            marker=dict(colors=CATEGORY_PAL[:len(catdf)], line=dict(color="#0B1220", width=2)),
            textfont=dict(size=11, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        ))
        apply_chart_theme(fig, height=440, show_legend=True)
        fig.update_layout(legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("Category Performance Details")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    catdf_s = catdf.sort_values("Total Sales")
    total_s = catdf["Total Sales"].sum()
    catdf_s["% Share"] = (catdf_s["Total Sales"] / total_s * 100).round(1)
    cat_tx = df.groupby("Category").size().reset_index(name="Transactions")
    catdf_s = catdf_s.merge(cat_tx, on="Category")
    fig = go.Figure(go.Bar(
        y=catdf_s["Category"], x=catdf_s["Total Sales"],
        orientation="h",
        marker_color=CATEGORY_PAL[:len(catdf_s)],
        text=[f"₹{v:,.0f}  ({p:.1f}%)" for v, p in zip(catdf_s["Total Sales"], catdf_s["% Share"])],
        textposition="outside", textfont=dict(size=10, color="#94A3B8"),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    apply_chart_theme(fig, height=300, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Product Summary Table")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    ps = df.groupby(["Product", "Category"]).agg(
        Transactions=("Invoice ID", "count"),
        Total_Sales=("Sales", "sum"),
        Avg_Sales=("Sales", "mean"),
        Avg_Qty=("Quantity", "mean"),
        Avg_Rating=("Rating", "mean"),
    ).round(2).reset_index().sort_values("Total_Sales", ascending=False)
    ps.columns = ["Product", "Category", "Transactions", "Total Sales", "Avg Sales", "Avg Qty", "Avg Rating"]
    ps["Total Sales"] = ps["Total Sales"].apply(lambda v: f"₹{v:,.2f}")
    ps["Avg Sales"]   = ps["Avg Sales"].apply(lambda v: f"₹{v:,.2f}")
    st.dataframe(ps.head(20), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — CUSTOMER ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "customer":
    ctdf  = sales_by_customer_type(df)
    gendf = sales_by_gender(df)
    ct_idx = ctdf.set_index("Customer Type")
    m_av = ct_idx.loc["Member", "Avg_Transaction"] if "Member" in ct_idx.index else 0
    n_av = ct_idx.loc["Normal", "Avg_Transaction"] if "Normal" in ct_idx.index else 0
    spender = "Normal" if n_av > m_av else "Member"

    cards = []
    for _, row in ctdf.iterrows():
        acc = "green" if row["Customer Type"] == "Member" else "amber"
        cards.append(kpi_card(
            "👤", row["Customer Type"],
            f"₹{row['Total_Sales']:,.0f}",
            f"{row['Transactions']} txns · Avg ₹{row['Avg_Transaction']:,.2f}", acc
        ))
    cards.append(kpi_card("💡", "Higher Spender", spender,
        f"₹{max(m_av,n_av):,.2f} avg / txn", "purple"))
    kpi_row(cards)

    col1, col2 = st.columns(2)
    with col1:
        section_header("Total Sales by Customer Type")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=ctdf["Customer Type"], y=ctdf["Total_Sales"],
            marker_color=["#3B82F6", "#10B981"],
            text=[f"₹{v:,.0f}" for v in ctdf["Total_Sales"]],
            textposition="outside", textfont=dict(size=11, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Avg. Transaction: Member vs Normal")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=ctdf["Customer Type"], y=ctdf["Avg_Transaction"],
            marker_color=["#F59E0B", "#EF4444"],
            text=[f"₹{v:,.2f}" for v in ctdf["Avg_Transaction"]],
            textposition="outside", textfont=dict(size=11, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Avg ₹%{y:,.2f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        section_header("Gender Split")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=gendf["Gender"], values=gendf["Total_Sales"],
            hole=0.5,
            marker=dict(colors=["#3B82F6","#F43F5E"], line=dict(color="#0B1220",width=2)),
            textfont=dict(size=12, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        ))
        apply_chart_theme(fig, height=300, show_legend=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        section_header("Avg. Transaction by Gender")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=gendf["Gender"], y=gendf["Avg_Transaction"],
            marker_color=["#3B82F6","#F43F5E"],
            text=[f"₹{v:,.2f}" for v in gendf["Avg_Transaction"]],
            textposition="outside", textfont=dict(size=11, color="#94A3B8"),
        ))
        apply_chart_theme(fig, height=300, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("Category Preference by Customer Type")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    ct_cat = df.groupby(["Customer Type","Category"])["Sales"].sum().reset_index()
    fig = px.bar(ct_cat, x="Category", y="Sales", color="Customer Type",
                 barmode="group",
                 color_discrete_sequence=["#3B82F6","#10B981"],
                 labels={"Sales": "Sales (₹)"})
    apply_chart_theme(fig, height=320)
    fig.update_traces(hovertemplate="<b>%{x}</b> — %{data.name}<br>₹%{y:,.0f}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Customer Intelligence Insight")
    diff = abs(m_av - n_av)
    insight_html = insight_card("👥", "Member vs Normal Spending",
        f"<strong>{'Normal customers' if n_av > m_av else 'Members'}</strong> have a higher average transaction "
        f"(₹{max(m_av,n_av):,.2f}) compared to {'Members' if n_av > m_av else 'Normal customers'} (₹{min(m_av,n_av):,.2f}). "
        f"The difference is <strong>₹{diff:,.2f}</strong> per transaction. "
        f"This suggests {'Normal customers generate slightly more revenue per visit.' if n_av > m_av else 'Membership programs drive slightly higher spending per visit.'}")
    st.markdown(insight_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 6 — PAYMENT ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "payment":
    paydf  = sales_by_payment(df)
    top_p  = paydf.iloc[0]
    tx     = total_transactions(df)

    cards = []
    for _, row in paydf.iterrows():
        col_map = {"UPI": "", "Card": "green", "Cash": "amber", "Net Banking": "purple"}
        acc = col_map.get(row["Payment"], "")
        cards.append(kpi_card(
            "💳", row["Payment"],
            f"{int(row['Transactions'])} txns",
            f"₹{row['Total_Sales']:,.0f} · {row['Transactions']/tx*100:.1f}%", acc
        ))
    kpi_row(cards)

    col1, col2 = st.columns(2)
    with col1:
        section_header("Transaction Share by Payment", "% of total transactions")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pay_colors = [PAYMENT_COLORS.get(p, "#3B82F6") for p in paydf["Payment"]]
        fig = go.Figure(go.Pie(
            labels=paydf["Payment"], values=paydf["Transactions"],
            hole=0.55,
            marker=dict(colors=pay_colors, line=dict(color="#0B1220",width=2)),
            textfont=dict(size=11, color="#F1F5F9"),
            hovertemplate="<b>%{label}</b><br>%{value} transactions (%{percent})<extra></extra>",
        ))
        apply_chart_theme(fig, height=340, show_legend=True)
        fig.update_layout(
            legend=dict(orientation="v", x=1.0, y=0.5),
            annotations=[dict(
                text=f"<b>{top_p['Payment']}</b><br>#{1}",
                x=0.5, y=0.5, font=dict(size=13, color="#F1F5F9"), showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Total Sales by Payment Method")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=paydf["Payment"], y=paydf["Total_Sales"],
            marker_color=pay_colors,
            text=[f"₹{v:,.0f}" for v in paydf["Total_Sales"]],
            textposition="outside", textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        apply_chart_theme(fig, height=340, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        section_header("Payment Usage by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pb2 = df.groupby(["Branch","Payment"]).size().reset_index(name="Transactions")
        fig = px.bar(pb2, x="Branch", y="Transactions", color="Payment",
                     barmode="group", color_discrete_map=PAYMENT_COLORS)
        apply_chart_theme(fig, height=300)
        fig.update_traces(hovertemplate="<b>Branch %{x}</b> — %{data.name}<br>%{y} transactions<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        section_header("Payment by Customer Type")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pc = df.groupby(["Customer Type","Payment"]).size().reset_index(name="Transactions")
        fig = px.bar(pc, x="Payment", y="Transactions", color="Customer Type",
                     barmode="group",
                     color_discrete_sequence=["#3B82F6","#10B981"])
        apply_chart_theme(fig, height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("Payment Summary Table")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pay_disp = paydf.copy()
    pay_disp["% Share"] = (pay_disp["Transactions"] / tx * 100).round(1).astype(str) + "%"
    pay_disp["Total_Sales"] = pay_disp["Total_Sales"].apply(lambda v: f"₹{v:,.2f}")
    pay_disp.columns = ["Payment Method", "Transactions", "Total Sales", "% Share"]
    st.dataframe(pay_disp, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    insight_html = insight_card("💳", "Payment Trend Insight",
        f"<strong>{top_p['Payment']}</strong> is the most-used payment method with "
        f"<strong>{int(top_p['Transactions'])}</strong> transactions ({top_p['Transactions']/tx*100:.1f}%). "
        f"It also generates the {'highest' if top_p['Total_Sales'] == paydf['Total_Sales'].max() else 'significant'} "
        f"revenue at <strong>₹{top_p['Total_Sales']:,.0f}</strong>. "
        f"Digital payments ({', '.join([p for p in paydf['Payment'] if p != 'Cash'])}) collectively represent "
        f"{(paydf[paydf['Payment']!='Cash']['Transactions'].sum()/tx*100):.1f}% of all transactions.")
    st.markdown(insight_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 7 — RATINGS
# ══════════════════════════════════════════════════════════════
elif page == "ratings":
    ov  = avg_rating(df)
    rc  = rating_by_category(df)
    rb  = rating_by_branch(df)

    cards = [
        kpi_card("⭐", "Avg. Rating", f"{ov} / 5", "Overall customer satisfaction",
                 "green" if ov >= 4.0 else "amber"),
        kpi_card("🔝", "Best Category", rc.iloc[0]["Category"],
                 f"Avg {rc.iloc[0]['Avg Rating']}", "green"),
        kpi_card("🏪", "Best Branch",
                 f"Branch {rb.iloc[0]['Branch']} ({rb.iloc[0]['City']})",
                 f"Avg {rb.iloc[0]['Avg Rating']}", "teal"),
        kpi_card("📊", "Rating Spread",
                 f"{df['Rating'].min():.1f} – {df['Rating'].max():.1f}",
                 "Min to Max range", "purple"),
    ]
    kpi_row(cards)

    col1, col2 = st.columns(2)
    with col1:
        section_header("Avg. Rating by Category")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=rc["Category"], y=rc["Avg Rating"],
            marker_color=CATEGORY_PAL[:len(rc)],
            text=[f"{v:.2f}" for v in rc["Avg Rating"]],
            textposition="outside", textfont=dict(size=11, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>",
        ))
        fig.add_hline(y=ov, line_dash="dash", line_color="#64748B", line_width=1.5,
                      annotation_text=f"Overall: {ov}",
                      annotation_font=dict(color="#94A3B8", size=11))
        apply_chart_theme(fig, height=320, show_legend=False)
        fig.update_layout(yaxis=dict(range=[0, 5.8]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        section_header("Avg. Rating by Branch")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        rb2 = rb.copy()
        rb2["Label"] = rb2.apply(lambda r: f"Branch {r['Branch']} ({r['City']})", axis=1)
        br_colors = [BRANCH_COLORS.get(b, "#3B82F6") for b in rb2["Branch"]]
        fig = go.Figure(go.Bar(
            x=rb2["Label"], y=rb2["Avg Rating"],
            marker_color=br_colors,
            text=[f"{v:.2f}" for v in rb2["Avg Rating"]],
            textposition="outside", textfont=dict(size=11, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>",
        ))
        fig.add_hline(y=ov, line_dash="dash", line_color="#64748B", line_width=1.5,
                      annotation_text=f"Overall: {ov}",
                      annotation_font=dict(color="#94A3B8", size=11))
        apply_chart_theme(fig, height=320, show_legend=False)
        fig.update_layout(yaxis=dict(range=[0, 5.8]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("Rating Distribution", "Frequency of each rating score")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    # Bin into 1,2,3,4,5
    df_rat = df.copy()
    df_rat["Rating Band"] = df_rat["Rating"].apply(
        lambda r: int(r) if r == int(r) else int(r)
    )
    dist = df_rat.groupby("Rating Band").size().reset_index(name="Count")
    all_bands = pd.DataFrame({"Rating Band": [1,2,3,4,5]})
    dist = all_bands.merge(dist, on="Rating Band", how="left").fillna(0)
    band_colors = ["#EF4444","#F59E0B","#F59E0B","#10B981","#3B82F6"]
    fig = go.Figure(go.Bar(
        x=dist["Rating Band"].astype(str), y=dist["Count"],
        marker_color=band_colors,
        text=dist["Count"].astype(int),
        textposition="outside", textfont=dict(size=11, color="#94A3B8"),
        hovertemplate="Rating %{x}<br>%{y} transactions<extra></extra>",
    ))
    apply_chart_theme(fig, height=280, show_legend=False)
    fig.update_layout(xaxis_title="Rating", yaxis_title="Transactions", bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Avg. Rating by Payment Method")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    rp = df.groupby("Payment")["Rating"].mean().round(2).reset_index()
    rp.columns = ["Payment", "Avg Rating"]
    pay_col2 = [PAYMENT_COLORS.get(p, "#3B82F6") for p in rp["Payment"]]
    fig = go.Figure(go.Bar(
        x=rp["Payment"], y=rp["Avg Rating"],
        marker_color=pay_col2,
        text=[f"{v:.2f}" for v in rp["Avg Rating"]],
        textposition="outside", textfont=dict(size=11, color="#94A3B8"),
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>",
    ))
    fig.add_hline(y=ov, line_dash="dash", line_color="#64748B", line_width=1.5,
                  annotation_text=f"Overall: {ov}",
                  annotation_font=dict(color="#94A3B8", size=11))
    apply_chart_theme(fig, height=280, show_legend=False)
    fig.update_layout(yaxis=dict(range=[0, 5.8]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    exp_txt = (f"Customers are broadly satisfied with an average of {ov}/5.0. "
               f"Maintenance of service quality is key." if ov >= 4.0 else
               f"Average rating {ov}/5.0 is below the 4.0 threshold. "
               f"Service quality improvements are recommended across branches.")
    st.markdown(insight_card("⭐", "Customer Experience Insight", exp_txt), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 8 — DATA QUALITY
# ══════════════════════════════════════════════════════════════
elif page == "quality":
    section_header("Data Quality & Validation", "Comprehensive dataset integrity assessment")

    # ── Compute validation metrics ──
    total_records = len(df_full)
    total_cols    = len(df_full.columns)
    missing       = int(df_full.isnull().sum().sum())
    duplicates    = int(df_full.duplicated().sum())
    inv_numeric   = int(df_full[["Quantity","Unit Price","Rating","Sales"]].isnull().sum().sum())
    inv_dates     = int(df_full["Date"].isnull().sum())
    inv_cats      = int((~df_full["Category"].isin(df_full["Category"].dropna().unique())).sum())

    # Sales consistency: Sales ≈ Quantity * Unit Price (within 1%)
    df_full["_calc"] = df_full["Quantity"] * df_full["Unit Price"]
    calc_err = int((((df_full["Sales"] - df_full["_calc"]).abs() / df_full["_calc"].clip(lower=0.01)) > 0.01).sum())
    df_full.drop(columns=["_calc"], inplace=True)

    # Invalid ratings
    inv_rating = int(((df_full["Rating"] < 1) | (df_full["Rating"] > 5)).sum())

    # Negative quantities or prices
    inv_qty   = int((df_full["Quantity"] <= 0).sum())
    inv_price = int((df_full["Unit Price"] <= 0).sum())

    def val_badge(n, label_ok="✓ VALID", label_bad="⚠ ISSUES"):
        if n == 0:
            return f'<span class="badge badge-green">{label_ok}</span>'
        return f'<span class="badge badge-amber">{label_bad}: {n}</span>'

    # ── Validation KPI grid ──
    st.markdown(f"""
    <div class="val-grid">
        <div class="val-card">
            <div class="val-card-label">Total Records</div>
            <div class="val-card-value">{total_records:,}</div>
            <div class="val-card-status"><span class="badge badge-blue">LOADED</span></div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Total Columns</div>
            <div class="val-card-value">{total_cols}</div>
            <div class="val-card-status"><span class="badge badge-blue">COLUMNS</span></div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Missing Values</div>
            <div class="val-card-value">{missing}</div>
            <div class="val-card-status">{val_badge(missing)}</div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Duplicate Records</div>
            <div class="val-card-value">{duplicates}</div>
            <div class="val-card-status">{val_badge(duplicates)}</div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Invalid Numerics</div>
            <div class="val-card-value">{inv_numeric}</div>
            <div class="val-card-status">{val_badge(inv_numeric)}</div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Invalid Dates</div>
            <div class="val-card-value">{inv_dates}</div>
            <div class="val-card-status">{val_badge(inv_dates)}</div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Sales Calc. Errors</div>
            <div class="val-card-value">{calc_err}</div>
            <div class="val-card-status">{val_badge(calc_err)}</div>
        </div>
        <div class="val-card">
            <div class="val-card-label">Invalid Ratings</div>
            <div class="val-card-value">{inv_rating}</div>
            <div class="val-card-status">{val_badge(inv_rating)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Detailed checks ──
    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
    section_header("Field-Level Validation", "Column-by-column data integrity results")

    checks = [
        ("Invoice ID",    "Unique identifier",          int(df_full["Invoice ID"].nunique()),        total_records, "Unique IDs == Records"),
        ("Date",          "Temporal coverage",           int(df_full["Date"].notnull().sum()),        total_records, "Non-null dates"),
        ("Branch",        "Valid branch codes",          int(df_full["Branch"].isin(["A","B","C","D"]).sum()), total_records, "A/B/C/D only"),
        ("Category",      "Category validity",           int(df_full["Category"].notnull().sum()),    total_records, "Non-null values"),
        ("Product",       "Product coverage",            int(df_full["Product"].notnull().sum()),     total_records, "Non-null values"),
        ("Quantity",      "Positive quantities",         int((df_full["Quantity"] > 0).sum()),        total_records, "> 0"),
        ("Unit Price",    "Positive unit prices",        int((df_full["Unit Price"] > 0).sum()),      total_records, "> 0"),
        ("Rating",        "Rating in [1,5]",             int(((df_full["Rating"]>=1)&(df_full["Rating"]<=5)).sum()), total_records, "1–5 range"),
        ("Sales",         "Sales = Qty × Price (±1%)",   total_records - calc_err,                    total_records, "Consistency check"),
        ("Payment",       "Known payment methods",       int(df_full["Payment"].isin(["UPI","Card","Cash","Net Banking"]).sum()), total_records, "Valid values"),
    ]

    rows_html = ""
    for field, desc, valid, total, note in checks:
        pct   = valid / total * 100 if total > 0 else 0
        badge = '<span class="badge badge-green">✓ VALID</span>' if valid == total else \
                f'<span class="badge badge-amber">⚠ {total-valid} issues</span>'
        rows_html += f"""
        <tr>
            <td style="font-weight:600;color:#E2E8F0;">{field}</td>
            <td style="color:#64748B;">{desc}</td>
            <td style="color:#F1F5F9;text-align:right;">{valid:,} / {total:,}</td>
            <td style="text-align:right;color:#64748B;">{pct:.1f}%</td>
            <td style="color:#64748B;">{note}</td>
            <td>{badge}</td>
        </tr>"""

    st.markdown(f"""
    <div class="chart-card">
        <table class="verify-table">
            <thead>
                <tr>
                    <th>Field</th><th>Check</th><th style="text-align:right">Valid / Total</th>
                    <th style="text-align:right">%</th><th>Criteria</th><th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # ── Manual Verification ──
    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
    section_header("Manual Result Verification",
                   "Comparison of calculated results against project manual expected values")

    results = verify_against_manual(df_full)

    verify_rows = []
    for key, r in results.items():
        desc = r["description"]
        match_keys = [k for k in r if k.endswith("_match") or k == "match"]
        all_ok = all(r[k] for k in match_keys)

        actual_vals   = {k: v for k,v in r.items() if k.startswith("actual")}
        expected_vals = {k: v for k,v in r.items() if k.startswith("expected")}

        actual_str   = "; ".join([f"{k.replace('actual_','')}: {v}" for k,v in actual_vals.items()])
        expected_str = "; ".join([f"{k.replace('expected_','')}: {v}" for k,v in expected_vals.items()])

        badge = '<span class="badge badge-green">✓ MATCH</span>' if all_ok else \
                '<span class="badge badge-amber">⚠ DIFFERENCE</span>'
        verify_rows += [(desc, actual_str, expected_str, badge, all_ok)]

    rows_html2 = ""
    for desc, actual, expected, badge, ok in verify_rows:
        rows_html2 += f"""
        <tr>
            <td style="font-weight:600;color:#E2E8F0;">{desc}</td>
            <td style="color:#94A3B8;font-size:12px;">{actual}</td>
            <td style="color:#64748B;font-size:12px;">{expected}</td>
            <td>{badge}</td>
        </tr>"""

    st.markdown(f"""
    <div class="chart-card">
        <table class="verify-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Actual (Calculated)</th>
                    <th>Manual Expected</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html2}</tbody>
        </table>
        <div style="font-size:11px;color:#475569;margin-top:12px;padding-top:10px;border-top:1px solid #1E293B;">
            ⓘ Discrepancies are shown as-is. Dataset values are preserved and not manipulated to match manual expectations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Raw Dataset Preview ──
    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
    section_header("Dataset Preview", f"{len(df_full):,} rows × {len(df_full.columns)} columns")
    with st.expander("View Raw Dataset", expanded=False):
        st.dataframe(df_full, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="dashboard-footer">
    Supermarket Sales Intelligence Dashboard &nbsp;·&nbsp;
    Data Analytics Project &nbsp;·&nbsp;
    Python &nbsp;•&nbsp; Pandas &nbsp;•&nbsp; Plotly &nbsp;•&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)
