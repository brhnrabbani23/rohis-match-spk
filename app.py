# =========================================================
# ROHIS-MATCH FINAL REDESIGN
# Catatan:
# - File ini melanjutkan redesign tampilan dari draft Claude.
# - Logic utama database, login, input penilaian, dan Profile Matching tetap dipertahankan.
# - Fokus perubahan: UI/UX, sidebar, topbar, card, dashboard, tabel, dan tampilan ranking.
# =========================================================

import streamlit as st
import mysql.connector
import pandas as pd
import time
import datetime

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & TEMA ROHIS (REDESIGN)
# ---------------------------------------------------------
st.set_page_config(page_title="ROHIS-MATCH", page_icon="🕌", layout="wide")

st.markdown("""
<style>
    /* ===== GLOBAL RESET & BASE ===== */
    [data-testid="stAppViewContainer"] {
        background-color: #091310 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #050a08 !important;
        border-right: 1px solid #12241f !important;
    }
    html, body, p, label, button, input, textarea, select, [data-testid="stMarkdownContainer"] {
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* FIX: tombol tutup/buka sidebar Streamlit memakai font ikon Material.
       Jangan sampai berubah menjadi tulisan seperti keyboard_double_arrow. */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    span[class*="material-symbols"],
    span[class*="Material"],
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span,
    button[aria-label*="sidebar"] span,
    button[title*="sidebar"] span {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 22px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: 'liga' !important;
        color: #10b981 !important;
    }

    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        color: #10b981 !important;
        max-width: 44px !important;
        overflow: hidden !important;
    }
    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #091310; }
    ::-webkit-scrollbar-thumb { background: #1b382e; border-radius: 4px; }

    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
    }
    div[data-testid="stSidebarUserContent"] label,
    div[data-testid="stSidebarUserContent"] p {
        color: #94a3b8 !important;
        font-size: 13px !important;
    }

    /* Sidebar menu sekarang memakai tombol kotak, bukan radio bullet */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        min-height: 40px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 8px 12px !important;
        margin: 2px 0 !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        transition: all .18s ease !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #94a3b8 !important;
        border: 1px solid transparent !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: #0a1e18 !important;
        color: #e2e8f0 !important;
        border: 1px solid #1b382e !important;
        transform: translateX(2px);
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #0a1e18 !important;
        color: #10b981 !important;
        border: 1px solid #1b382e !important;
        border-left: 4px solid #10b981 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: #0d2b20 !important;
        color: #eab308 !important;
        border-color: #10b981 !important;
        border-left-color: #eab308 !important;
    }

    /* Fallback: jika masih ada radio, bullet disembunyikan dan label dibuat kotak */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        padding: 9px 12px !important;
        margin: 4px 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #0a1e18 !important;
        border-color: #1b382e !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #0a1e18 !important;
        border-color: #1b382e !important;
        border-left: 4px solid #10b981 !important;
        color: #10b981 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* ===== PRIMARY BUTTONS ===== */
    button[kind="primary"] {
        background-color: #10b981 !important;
        color: #050a08 !important;
        border: 1px solid #059669 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #eab308 !important;
        color: #050a08 !important;
        border-color: #ca8a04 !important;
    }

    /* ===== SECONDARY BUTTONS ===== */
    button[kind="secondary"] {
        background-color: #0d1f19 !important;
        color: #10b981 !important;
        border: 1px solid #1b382e !important;
        border-radius: 8px !important;
        min-height: 44px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #1b382e !important;
        color: #eab308 !important;
        border-color: #eab308 !important;
    }

    /* ===== INPUT, SELECT, TEXTAREA ===== */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        background-color: #0d1f19 !important;
        border-color: #1b382e !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within {
        border-color: #10b981 !important;
    }
    div[data-baseweb="popover"] {
        background-color: #0d1f19 !important;
        border: 1px solid #1b382e !important;
    }
    li[role="option"]:hover {
        background-color: #1b382e !important;
    }

    /* ===== METRICS ===== */
    div[data-testid="stMetricValue"] {
        color: #eab308 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 12px !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    [data-testid="stMetric"] {
        background: #0a1e18 !important;
        border: 1px solid #12241f !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
    }

    /* ===== TABS ===== */
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #64748b !important;
        border-bottom: 2px solid transparent !important;
        font-size: 13px !important;
    }
    button[aria-selected="true"][data-baseweb="tab"] {
        color: #10b981 !important;
        border-bottom-color: #10b981 !important;
        font-weight: 600 !important;
        background: transparent !important;
    }
    div[data-testid="stTabs"] {
        border-bottom: 1px solid #12241f !important;
    }

    /* ===== DATAFRAME / TABLE ===== */
    [data-testid="stDataFrame"] {
        border: 1px solid #12241f !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    th {
        background-color: #0a1e18 !important;
        color: #10b981 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-bottom: 1px solid #1b382e !important;
    }
    td {
        background-color: #091310 !important;
        border-bottom: 1px solid #0d1f19 !important;
        font-size: 13px !important;
    }
    tr:hover td {
        background-color: #0d1f19 !important;
    }
    [data-testid="stDataFrameResizable"] {
        background: #091310 !important;
    }

    /* ===== ALERTS & NOTIFICATIONS ===== */
    div[data-testid="stNotification"],
    div[data-testid="stAlert"] {
        background-color: #0a1e18 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"][data-baseweb="notification"] {
        border-left: 4px solid #10b981 !important;
    }

    /* ===== EXPANDER ===== */
    details {
        background: #0a1e18 !important;
        border: 1px solid #12241f !important;
        border-radius: 8px !important;
    }
    summary {
        color: #10b981 !important;
        font-weight: 500 !important;
    }

    /* ===== FORMS ===== */
    [data-testid="stForm"] {
        background: #0a1e18 !important;
        border: 1px solid #12241f !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    /* ===== DIALOG / MODAL ===== */
    div[role="dialog"] {
        background: #050a08 !important;
        border: 1px solid #1b382e !important;
        border-radius: 12px !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    a[data-testid="stDownloadButton"] button {
        background-color: #0d1f19 !important;
        color: #10b981 !important;
        border: 1px solid #1b382e !important;
    }

    /* ===== BOLD TEXT ===== */
    strong, b {
        color: #eab308 !important;
    }

    /* ===== CAPTION / SMALL TEXT ===== */
    small, [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border-color: #12241f !important;
    }

    /* ===== SPINNER ===== */
    div[data-testid="stSpinner"] {
        color: #10b981 !important;
    }

    /* ===== SELECTBOX OPTIONS ===== */
    ul[data-testid="stSelectboxVirtualDropdown"] li {
        background: #0d1f19 !important;
        color: #e2e8f0 !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
        background: #1b382e !important;
        color: #10b981 !important;
    }

    /* ===== CHARTS (bar_chart) ===== */
    [data-testid="stVegaLiteChart"] {
        background: #0a1e18 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. HELPER: KOMPONEN UI ISLAMI
# ---------------------------------------------------------
def render_page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="
        background: #0a1e18;
        border: 1px solid #12241f;
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
    ">
        <div style="
            width: 46px; height: 46px;
            background: #0d2b20;
            border: 1.5px solid #1D9E75;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            position: relative;
            flex-shrink: 0;
        ">
            {icon}
            <div style="position:absolute;top:-2px;left:-2px;width:6px;height:6px;border:1px solid #10b981;border-radius:1px;"></div>
            <div style="position:absolute;top:-2px;right:-2px;width:6px;height:6px;border:1px solid #10b981;border-radius:1px;"></div>
            <div style="position:absolute;bottom:-2px;left:-2px;width:6px;height:6px;border:1px solid #10b981;border-radius:1px;"></div>
            <div style="position:absolute;bottom:-2px;right:-2px;width:6px;height:6px;border:1px solid #10b981;border-radius:1px;"></div>
        </div>
        <div>
            <div style="font-size:17px;font-weight:600;color:#e2e8f0;margin-bottom:3px;">{title}</div>
            <div style="font-size:12px;color:#64748b;">{subtitle}</div>
        </div>
        <div style="margin-left:auto;font-size:24px;color:#eab308;opacity:0.4;letter-spacing:6px;">❋ ✦ ❋</div>
    </div>
    """, unsafe_allow_html=True)


def render_divider_arabic():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin:8px 0 16px;">
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#1D9E75,transparent);"></div>
        <span style="color:#eab308;opacity:0.5;font-size:14px;">✦</span>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#1D9E75,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def render_card_start(title: str = "", icon: str = ""):
    header = ""
    if title:
        header = f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
            <span style="font-size:15px;">{icon}</span>
            <span style="font-size:13px;font-weight:500;color:#cbd5e1;">{title}</span>
            <div style="margin-left:auto;width:6px;height:6px;border-radius:50%;background:#10b981;"></div>
        </div>
        """
    st.markdown(f"""
    <div style="
        background:#0a1e18;
        border:1px solid #12241f;
        border-radius:10px;
        padding:16px;
        margin-bottom:12px;
    ">
        {header}
    """, unsafe_allow_html=True)


def render_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def render_geo_badge(label: str, color: str = "#10b981"):
    st.markdown(f"""
    <span style="
        font-size:11px;
        background:{color}18;
        color:{color};
        border:1px solid {color}40;
        border-radius:20px;
        padding:3px 10px;
        font-weight:500;
    ">{label}</span>
    """, unsafe_allow_html=True)


def render_sidebar_logo():
    st.markdown("""
    <div style="
        padding: 18px 16px 14px;
        border-bottom: 1px solid #12241f;
        margin-bottom: 4px;
    ">
        <div style="font-size:10px;color:#1D9E75;letter-spacing:2.5px;margin-bottom:5px;font-weight:500;">
            بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
        </div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <polygon points="10,1 12,7 18,7 13,11 15,17 10,13 5,17 7,11 2,7 8,7"
                    fill="none" stroke="#10b981" stroke-width="1.2"/>
                <circle cx="10" cy="10" r="2.2" fill="#eab308" opacity="0.85"/>
            </svg>
            <span style="font-size:19px;font-weight:700;color:#10b981;letter-spacing:1px;">ROHIS-MATCH</span>
        </div>
        <div style="font-size:11px;color:#eab308;font-weight:500;margin-bottom:10px;">
            SMPN 87 Jakarta
        </div>
        <div style="
            height:3px;
            background: repeating-linear-gradient(
                90deg,
                #10b981 0px, #10b981 8px,
                #1D9E75 8px, #1D9E75 14px,
                #eab308 14px, #eab308 18px,
                #1D9E75 18px, #1D9E75 24px
            );
            opacity:0.55;
            border-radius:2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)




def render_sidebar_menu(menu_items, key_prefix="menu"):
    """Render menu sidebar dalam bentuk kotak tombol, bukan radio bullet."""
    active_menu = st.session_state.get('menu_aktif') or menu_items[0]
    if active_menu not in menu_items:
        active_menu = menu_items[0]
        st.session_state['menu_aktif'] = active_menu

    for idx, item in enumerate(menu_items):
        is_active = active_menu == item
        button_type = "primary" if is_active else "secondary"
        safe_key = f"{key_prefix}_{idx}_{item.replace(' ', '_').replace('⭐','star').replace('🏠','home').replace('👥','people').replace('📝','input').replace('⚙️','settings')}"
        if st.button(item, key=safe_key, type=button_type, use_container_width=True):
            if st.session_state.get('menu_aktif') != item:
                catat_log(f"Membuka halaman {item}")
            st.session_state['menu_aktif'] = item
            st.rerun()


def render_sidebar_access_note(mode="public"):
    if mode == "login":
        title = "Portal Login Khusus"
        desc = "Halaman ini hanya digunakan oleh Pembina dan Pengurus untuk mengelola data, input penilaian, dan melihat hasil rekomendasi."
        icon = "🔐"
        border = "#10b981"
    else:
        title = "Akses Pengguna"
        desc = "Menu publik dapat dilihat tanpa akun. Login hanya untuk Pengurus dan Pembina Rohis."
        icon = "👥"
        border = "#eab308"
    st.markdown(f"""
    <div style="background:#0a1e18;border:1px solid #12241f;border-left:4px solid {border};border-radius:10px;padding:13px 14px;margin-top:12px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:16px;">{icon}</span>
            <span style="font-size:12px;font-weight:700;color:#e2e8f0;">{title}</span>
        </div>
        <div style="font-size:11px;color:#94a3b8;line-height:1.65;">{desc}</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;">
            <span style="font-size:10px;background:#0d2b20;color:#10b981;border:1px solid #1b382e;border-radius:999px;padding:3px 8px;">Pembina</span>
            <span style="font-size:10px;background:#201a05;color:#eab308;border:1px solid #3b2f0a;border-radius:999px;padding:3px 8px;">Pengurus</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_user_card(username, role_aktif):
    inisial = username[0].upper() if username else "?"
    role_label = (role_aktif or "pengguna").upper()
    role_color = "#10b981" if role_aktif == "pembina" else "#eab308"
    st.markdown(f"""
    <div style="background:#0a1e18;border:1px solid #12241f;border-radius:12px;padding:14px;margin-top:10px;">
        <div style="font-size:10px;color:#3d6b5a;text-transform:uppercase;letter-spacing:1.4px;margin-bottom:10px;">Akun Aktif</div>
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="
                width:38px;height:38px;border-radius:12px;
                background:#0d2b20;border:1.5px solid {role_color};
                display:flex;align-items:center;justify-content:center;
                font-size:14px;color:{role_color};font-weight:800;flex-shrink:0;
            ">{inisial}</div>
            <div style="min-width:0;">
                <div style="font-size:12px;color:#e2e8f0;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{username}</div>
                <div style="font-size:10px;color:{role_color};font-weight:700;text-transform:uppercase;margin-top:2px;">{role_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_topbar(menu_name: str):
    # Aman untuk halaman publik: saat belum login, role/username bernilai None.
    role = (st.session_state.get('role') or 'PUBLIK').upper()
    username = st.session_state.get('username') or 'Tamu'
    role_color = "#10b981" if role == "PEMBINA" else "#eab308"

    st.markdown(f"""
    <div style="
        background:#091310;
        border-bottom:1px solid #12241f;
        padding:12px 0px 12px 4px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:16px;
    ">
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:3px;height:22px;background:#10b981;border-radius:2px;"></div>
            <span style="font-size:16px;font-weight:600;color:#e2e8f0;">{menu_name}</span>
            <span style="font-size:12px;color:#3d6b5a;">· Tahun Ajaran 2026</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="
                font-size:11px;
                background:{role_color}18;
                color:{role_color};
                border:1px solid {role_color}40;
                border-radius:20px;
                padding:4px 12px;
                font-weight:500;
            ">🔐 {role} — {username}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card_custom(label: str, value: str, sub: str = "", accent: str = "#10b981", icon: str = "📊"):
    st.markdown(f"""
    <div style="
        background:#0a1e18;
        border:1px solid #12241f;
        border-radius:10px;
        padding:16px 18px;
        position:relative;
        overflow:hidden;
        min-height:136px;
    ">
        <div style="position:absolute;top:0;left:0;right:0;height:2.5px;background:{accent};border-radius:2px 2px 0 0;"></div>
        <div style="font-size:11px;color:#cbd5e1;margin-bottom:10px;display:flex;align-items:center;gap:6px;font-weight:500;">
            <span style="font-size:13px;">{icon}</span> {label}
        </div>
        <div style="font-size:26px;font-weight:700;color:#eab308;line-height:1.2;max-width:78%;word-wrap:break-word;">{value}</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:8px;max-width:80%;line-height:1.5;">{sub}</div>
        <div style="
            position:absolute;right:16px;top:50%;transform:translateY(-50%);
            width:52px;height:52px;border-radius:14px;
            display:flex;align-items:center;justify-content:center;
            background:{accent}1f;border:1px solid {accent}55;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            font-size:24px;
        ">{icon}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. KONEKSI DATABASE (CONNECTION POOLING)
# ---------------------------------------------------------
# ---------------------------------------------------------
# 3. KONEKSI DATABASE (MULTI-USER ISOLATION)
# ---------------------------------------------------------

def create_new_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        database=st.secrets["DB_NAME"],
        use_pure=True,
        autocommit=True # Wajib agar data langsung tersimpan
    )

# 1. Simpan koneksi secara eksklusif untuk masing-masing user (Private Session)
if 'db_conn' not in st.session_state:
    st.session_state['db_conn'] = create_new_connection()

conn = st.session_state['db_conn']

# 2. Fitur Auto-Reconnect: Cek denyut nadi koneksi sebelum ngapa-ngapain
try:
    conn.ping(reconnect=True, attempts=3, delay=1)
except Exception:
    # Kalau terowongan diputus karena user kelamaan AFK, otomatis bikin baru!
    st.session_state['db_conn'] = create_new_connection()
    conn = st.session_state['db_conn']

# 3. Bikin kursor khusus untuk eksekusi query
cursor = conn.cursor(dictionary=True)


# ---------------------------------------------------------
# 4. SESSION STATE & LOGGING
# ---------------------------------------------------------
defaults = {
    'logged_in': False,
    'username': None,
    'role': None,
    'menu_aktif': "🏠 Dashboard",
    'menu_pilihan_key': "🏠 Dashboard",
    'login_attempts': 0,
    'lockout_until': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def catat_log(aksi):
    role_saat_ini = st.session_state['role'] if st.session_state['logged_in'] else 'anggota'
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO log_aktivitas (waktu, role, aksi) VALUES (%s, %s, %s)",
            (waktu, role_saat_ini, aksi)
        )
        conn.commit()
    except Exception:
        pass


def proses_logout():
    catat_log("Keluar (logout) dari sistem")
    for k in ['logged_in', 'username', 'role']:
        st.session_state[k] = False if k == 'logged_in' else None
    st.session_state['menu_aktif'] = "🏠 Dashboard"
    st.session_state['menu_pilihan_key'] = "🏠 Dashboard"
    st.rerun()


@st.dialog("⚠️ Konfirmasi Logout")
def dialog_konfirmasi_logout():
    st.markdown("""
    <div style="text-align:center;padding:10px 0;">
        <div style="font-size:36px;margin-bottom:10px;">🚪</div>
        <p style="color:#94a3b8;">Apakah Anda yakin ingin keluar dari sistem?</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Ya, Keluar", type="primary", use_container_width=True):
            proses_logout()
    with c2:
        if st.button("Batal", use_container_width=True):
            st.rerun()


# ---------------------------------------------------------
# 5. HALAMAN LOGIN
# ---------------------------------------------------------
def halaman_login():
    st.markdown("""
    <div style="text-align:center;margin:20px 0 10px;">
        <div style="font-size:48px;margin-bottom:10px;">🕌</div>
        <h2 style="color:#10b981;font-size:22px;font-weight:600;margin-bottom:4px;">Portal Login ROHIS-MATCH</h2>
        <p style="color:#64748b;font-size:13px;">Sistem Pendukung Keputusan Divisi Rohis SMPN 87 Jakarta</p>
    </div>
    """, unsafe_allow_html=True)

    render_divider_arabic()

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div style="
            background:#0a1e18;
            border:1px solid #1b382e;
            border-top:3px solid #10b981;
            border-radius:12px;
            padding:24px;
        ">
            <div style="font-size:15px;font-weight:600;color:#10b981;margin-bottom:16px;text-align:center;">
                👤 Masuk ke Sistem
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            input_user = st.text_input("Username", placeholder="Masukkan username...")
            input_pass = st.text_input("Password", type="password", placeholder="Masukkan password...")
            btn_login = st.form_submit_button("🔐 Login", type="primary", use_container_width=True)

            if btn_login:
                if time.time() < st.session_state['lockout_until']:
                    sisa = int(st.session_state['lockout_until'] - time.time())
                    st.error(f"🛑 Sistem terkunci! Coba lagi dalam **{sisa} detik**.")
                    catat_log("Mencoba login saat masa penalti")
                else:
                    if not input_user or not input_pass:
                        st.warning("⚠️ Username dan Password tidak boleh kosong!")
                    else:
                        cursor.execute(
                            "SELECT * FROM user WHERE username = %s AND password = %s",
                            (input_user, input_pass)
                        )
                        user_data = cursor.fetchone()

                        if user_data:
                            st.session_state.update({
                                'login_attempts': 0,
                                'lockout_until': 0,
                                'logged_in': True,
                                'username': user_data['username'],
                                'role': user_data['role'],
                                'menu_aktif': "🏠 Dashboard",
                                'menu_pilihan_key': "🏠 Dashboard",
                            })
                            catat_log(f"Login berhasil: {user_data['username']}")
                            st.success("✅ Login berhasil! Memuat sistem...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.session_state['login_attempts'] += 1
                            catat_log(f"Gagal login ke-{st.session_state['login_attempts']}: {input_user}")
                            if st.session_state['login_attempts'] >= 3:
                                st.session_state['lockout_until'] = time.time() + 30
                                st.error("⚠️ Terlalu banyak percobaan gagal! Sistem terkunci 30 detik.")
                            else:
                                sisa = 3 - st.session_state['login_attempts']
                                st.error(f"❌ Username atau Password salah! (Sisa kesempatan: **{sisa}**)")


# ---------------------------------------------------------
# 6. STATISTIK
# ---------------------------------------------------------
def get_statistik():
    cursor.execute("SELECT COUNT(kd_siswa) AS total FROM siswa")
    total_siswa = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(id_divisi) AS total FROM divisi")
    total_divisi = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(id_kriteria) AS total FROM kriteria")
    total_kriteria = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(DISTINCT kd_siswa) AS total FROM hasil_ranking")
    total_ranked = cursor.fetchone()['total']
    return total_siswa, total_divisi, total_kriteria, total_ranked


# ---------------------------------------------------------
# 7. HALAMAN DASHBOARD
# ---------------------------------------------------------
def halaman_dashboard():
    if st.session_state['logged_in']:
        render_topbar("🏠 Dashboard")

        role = st.session_state['role'].lower()
        nama = st.session_state['username']

        if role == 'pembina':
            greeting = f"Assalamu'alaikum, Bapak/Ibu {nama}"
            sub = "Selamat datang kembali di Sistem Pendukung Keputusan Divisi Rohis"
        else:
            greeting = f"Assalamu'alaikum, Kak {nama}"
            sub = "Selamat datang, Pengurus Rohis SMPN 87 Jakarta"

        render_page_header("🕌", greeting, sub)
    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px;">
            <div style="font-size:40px;margin-bottom:8px;">🕌</div>
            <h1 style="color:#10b981;font-size:24px;font-weight:600;">ROHIS-MATCH</h1>
            <p style="color:#64748b;font-size:13px;">Sistem Pendukung Keputusan Penempatan Divisi</p>
        </div>
        """, unsafe_allow_html=True)

    render_divider_arabic()

    st.markdown("##### 📊 Ringkasan Data", unsafe_allow_html=True)
    total_siswa, total_divisi, total_kriteria, total_ranked = get_statistik()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card_custom("Total Anggota", f"{total_siswa}", "Siswa terdaftar", "#10b981", "👥")
    with c2:
        render_metric_card_custom("Total Divisi", f"{total_divisi}", "Divisi tersedia", "#eab308", "🏷️")
    with c3:
        render_metric_card_custom("Kriteria Penilaian", f"{total_kriteria}", "Aspek penilaian", "#1D9E75", "📋")
    with c4:
        pct = f"{(total_ranked/total_siswa*100):.0f}%" if total_siswa else "0%"
        render_metric_card_custom("Sudah Diranking", f"{total_ranked}", f"dari {total_siswa} siswa ({pct})", "#059669", "⭐")

    render_divider_arabic()

    col_chart, col_rank = st.columns([2, 1])

    with col_chart:
        st.markdown("""
        <div style="
            background:#0a1e18;border:1px solid #12241f;
            border-radius:10px;padding:16px;margin-bottom:12px;
        ">
            <div style="font-size:13px;font-weight:500;color:#cbd5e1;margin-bottom:10px;">
                📈 Sebaran Anggota per Divisi
            </div>
        </div>
        """, unsafe_allow_html=True)

        cursor.execute("""
            SELECT d.nama_divisi, COUNT(h.id_ranking) as jumlah
            FROM divisi d
            LEFT JOIN hasil_ranking h ON d.id_divisi = h.id_divisi
            GROUP BY d.id_divisi
        """)
        data_sebaran = cursor.fetchall()
        if data_sebaran:
            df_sebaran = pd.DataFrame(data_sebaran)
            df_sebaran = df_sebaran.rename(columns={'nama_divisi': 'Divisi', 'jumlah': 'Jumlah Siswa'})
            df_sebaran = df_sebaran.set_index('Divisi')
            try:
                st.bar_chart(df_sebaran, color="#10b981")
            except TypeError:
                st.bar_chart(df_sebaran)
        else:
            st.info("Belum ada data penempatan divisi.")

    with col_rank:
        st.markdown("""
        <div style="
            background:#0a1e18;border:1px solid #12241f;
            border-radius:10px;padding:16px;
        ">
            <div style="font-size:13px;font-weight:500;color:#cbd5e1;margin-bottom:12px;">
                🏆 Top Ranking
            </div>
        """, unsafe_allow_html=True)

        cursor.execute("""
            SELECT s.nama_siswa, s.kelas,
                   GROUP_CONCAT(d.nama_divisi SEPARATOR ' / ') as nama_divisi,
                   h.skor_akhir
            FROM hasil_ranking h
            JOIN siswa s ON h.kd_siswa = s.kd_siswa
            JOIN divisi d ON h.id_divisi = d.id_divisi
            GROUP BY s.kd_siswa, s.nama_siswa, s.kelas, h.skor_akhir
            ORDER BY h.skor_akhir DESC
            LIMIT 5
        """)
        top_list = cursor.fetchall()

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        if top_list:
            for i, siswa in enumerate(top_list):
                inisial = "".join([n[0].upper() for n in siswa['nama_siswa'].split()[:2]])
                skor_pct = (float(siswa['skor_akhir']) / 5.0) * 100
                divisi = siswa['nama_divisi'].split(" / ")[0]
                border_color = "#eab308" if i == 0 else "#1b382e"
                text_color = "#eab308" if i == 0 else "#10b981"
                st.markdown(f"""
                <div style="
                    display:flex;align-items:center;gap:8px;
                    background:#0d1f19;border-radius:8px;
                    padding:8px 10px;margin-bottom:6px;
                    border:1px solid {border_color};
                ">
                    <span style="font-size:14px;width:20px;">{medals[i]}</span>
                    <div style="
                        width:28px;height:28px;border-radius:50%;
                        background:#0d2b20;border:1.5px solid {border_color};
                        display:flex;align-items:center;justify-content:center;
                        font-size:10px;color:{text_color};font-weight:600;flex-shrink:0;
                    ">{inisial}</div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-size:11px;color:#cbd5e1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{siswa['nama_siswa']}</div>
                        <div style="font-size:10px;color:#64748b;">{divisi}</div>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:{text_color};">{skor_pct:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada data ranking.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Log aktivitas terbaru (hanya jika login)
    if st.session_state['logged_in']:
        render_divider_arabic()
        st.markdown("##### 🕐 Aktivitas Terbaru", unsafe_allow_html=True)
        try:
            cursor.execute("SELECT waktu, role, aksi FROM log_aktivitas ORDER BY waktu DESC LIMIT 6")
            logs = cursor.fetchall()
            if logs:
                st.markdown("""
                <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:16px;">
                """, unsafe_allow_html=True)
                for log in logs:
                    color = "#10b981" if "berhasil" in log['aksi'].lower() else "#eab308" if "simpan" in log['aksi'].lower() or "input" in log['aksi'].lower() else "#64748b"
                    st.markdown(f"""
                    <div style="display:flex;gap:12px;align-items:flex-start;padding:7px 0;border-bottom:1px solid #0d1f19;">
                        <div style="width:8px;height:8px;border-radius:50%;background:{color};margin-top:4px;flex-shrink:0;"></div>
                        <div style="flex:1;">
                            <div style="font-size:12px;color:#94a3b8;">{log['aksi']}</div>
                            <div style="font-size:10px;color:#3d6b5a;margin-top:2px;">{log['waktu']} · {log['role'].upper()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception:
            pass


# ---------------------------------------------------------
# 8. HALAMAN DATA SISWA (CRUD)
# ---------------------------------------------------------
def halaman_data_siswa():
    render_topbar("👥 Data Anggota")
    render_page_header("👥", "Manajemen Data Anggota", "Kelola data anggota Rohis yang akan diseleksi penempatan divisinya")

    list_kelas = ["7.1","7.2","7.3","7.4","7.5","7.6","8.1","8.2","8.3","8.4","8.5","8.6"]

    cursor.execute("SELECT kd_siswa, nama_siswa, kelas FROM siswa ORDER BY kd_siswa DESC")
    data_siswa = cursor.fetchall()

    st.markdown("""
    <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:16px;margin-bottom:12px;">
        <div style="font-size:13px;font-weight:500;color:#10b981;margin-bottom:10px;">📋 Daftar Anggota Terdaftar</div>
    """, unsafe_allow_html=True)

    if data_siswa:
        df_siswa = pd.DataFrame(data_siswa)
        df_siswa.columns = ['ID Siswa', 'Nama Lengkap', 'Kelas']
        st.dataframe(df_siswa, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data anggota yang terdaftar.")
        df_siswa = pd.DataFrame()

    st.markdown("</div>", unsafe_allow_html=True)

    render_divider_arabic()
    tab_tambah, tab_edit, tab_hapus = st.tabs(["➕ Tambah Data", "✏️ Edit Data", "🗑️ Hapus Data"])

    with tab_tambah:
        with st.form("form_tambah_siswa"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#10b981;margin-bottom:10px;'>Masukkan Data Anggota Baru</div>", unsafe_allow_html=True)
            input_nama = st.text_input("Nama Lengkap Siswa", placeholder="Contoh: Ahmad Fauzan")
            input_kelas = st.selectbox("Kelas", list_kelas)
            btn = st.form_submit_button("💾 Simpan ke Database", type="primary")
            if btn:
                if not input_nama.strip():
                    st.error("❌ Nama siswa tidak boleh kosong!")
                else:
                    try:
                        cursor.execute("INSERT INTO siswa (nama_siswa, kelas) VALUES (%s, %s)", (input_nama, input_kelas))
                        conn.commit()
                        catat_log(f"Menambahkan data siswa: {input_nama} ({input_kelas})")
                        st.success(f"✅ Data **{input_nama}** berhasil ditambahkan!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_edit:
        if not df_siswa.empty:
            opsi = df_siswa['ID Siswa'].astype(str) + " - " + df_siswa['Nama Lengkap']
            pilih = st.selectbox("Pilih Anggota yang akan diedit:", opsi)
            kd = pilih.split(" - ")[0]
            cursor.execute("SELECT * FROM siswa WHERE kd_siswa = %s", (kd,))
            lama = cursor.fetchone()
            with st.form("form_edit_siswa"):
                edit_nama = st.text_input("Nama Lengkap", value=lama['nama_siswa'])
                try:
                    idx = list_kelas.index(lama['kelas'])
                except ValueError:
                    idx = 0
                edit_kelas = st.selectbox("Kelas", list_kelas, index=idx)
                if st.form_submit_button("✏️ Update Data", type="primary"):
                    if not edit_nama.strip():
                        st.error("❌ Nama tidak boleh kosong!")
                    else:
                        cursor.execute("UPDATE siswa SET nama_siswa=%s, kelas=%s WHERE kd_siswa=%s", (edit_nama, edit_kelas, kd))
                        conn.commit()
                        catat_log(f"Mengubah data siswa ID {kd} → {edit_nama} ({edit_kelas})")
                        st.success("✅ Data berhasil diperbarui!")
                        time.sleep(1)
                        st.rerun()
        else:
            st.warning("Tidak ada data yang bisa diedit.")

    with tab_hapus:
        if not df_siswa.empty:
            opsi = df_siswa['ID Siswa'].astype(str) + " - " + df_siswa['Nama Lengkap']
            pilih = st.selectbox("Pilih Anggota yang akan dihapus:", opsi)
            kd = pilih.split(" - ")[0]
            nama_hapus = pilih.split(" - ")[1]
            st.markdown(f"""
            <div style="background:#180a0a;border:1px solid #3b1515;border-left:4px solid #ef4444;
                        border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                <div style="font-size:13px;color:#fca5a5;font-weight:500;">⚠️ Peringatan</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px;">
                    Menghapus <strong style="color:#fca5a5;">{nama_hapus}</strong> juga akan menghapus seluruh data nilainya. Tindakan ini tidak dapat dibatalkan.
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("form_hapus_siswa"):
                if st.form_submit_button("🗑️ Ya, Hapus Permanen", type="primary"):
                    cursor.execute("DELETE FROM siswa WHERE kd_siswa = %s", (kd,))
                    conn.commit()
                    catat_log(f"Menghapus siswa: {nama_hapus}")
                    st.success("✅ Data berhasil dihapus.")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Tidak ada data yang bisa dihapus.")


# ---------------------------------------------------------
# 9. HALAMAN PENGATURAN AKUN
# ---------------------------------------------------------
def halaman_profil():
    render_topbar("⚙️ Pengaturan Akun")
    render_page_header("⚙️", "Pengaturan Akun", "Kelola kredensial akun Anda untuk menjaga keamanan sistem")

    uname = st.session_state['username']
    cursor.execute("SELECT * FROM user WHERE username = %s", (uname,))
    user_info = cursor.fetchone()

    if not user_info:
        st.error("Gagal memuat data akun dari database.")
        return

    tab_info, tab_user, tab_pass = st.tabs(["ℹ️ Info Akun", "✏️ Ubah Username", "🔒 Ubah Password"])

    with tab_info:
        st.markdown(f"""
        <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:20px;max-width:480px;">
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
                <div style="
                    width:52px;height:52px;border-radius:50%;
                    background:#0d2b20;border:2px solid #10b981;
                    display:flex;align-items:center;justify-content:center;
                    font-size:20px;color:#10b981;font-weight:700;
                ">{user_info['username'][0].upper()}</div>
                <div>
                    <div style="font-size:16px;font-weight:600;color:#e2e8f0;">{user_info['username']}</div>
                    <div style="
                        font-size:11px;margin-top:4px;padding:2px 10px;
                        background:#0d2b20;color:#10b981;border:1px solid #1D9E75;
                        border-radius:20px;display:inline-block;font-weight:500;
                    ">{user_info['role'].upper()}</div>
                </div>
            </div>
            <div style="border-top:1px solid #12241f;padding-top:14px;">
                <div style="font-size:12px;color:#64748b;margin-bottom:6px;">Hak akses Anda menentukan batasan manipulasi data kriteria dan perhitungan algoritma SPK.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_user:
        with st.form("form_ubah_username"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#10b981;margin-bottom:10px;'>Ganti Username Akun</div>", unsafe_allow_html=True)
            new_user = st.text_input("Username Baru")
            if st.form_submit_button("🔄 Perbarui Username", type="primary"):
                if not new_user.strip():
                    st.error("❌ Username baru tidak boleh kosong!")
                elif new_user == uname:
                    st.warning("Username baru sama dengan yang sekarang.")
                else:
                    cursor.execute("SELECT * FROM user WHERE username = %s", (new_user,))
                    if cursor.fetchone():
                        st.error("🛑 Username sudah dipakai akun lain!")
                    else:
                        try:
                            cursor.execute("UPDATE user SET username=%s WHERE username=%s", (new_user, uname))
                            conn.commit()
                            catat_log(f"Mengubah username → {new_user}")
                            st.session_state['username'] = new_user
                            st.success("✅ Username berhasil diubah!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    with tab_pass:
        with st.form("form_ubah_password"):
            st.markdown("<div style='font-size:14px;font-weight:500;color:#10b981;margin-bottom:10px;'>Ganti Kata Sandi</div>", unsafe_allow_html=True)
            old_p = st.text_input("Password Lama", type="password")
            new_p = st.text_input("Password Baru", type="password")
            conf_p = st.text_input("Konfirmasi Password Baru", type="password")
            if st.form_submit_button("🔒 Perbarui Password", type="primary"):
                if old_p != user_info['password']:
                    st.error("❌ Password lama salah!")
                elif not new_p.strip():
                    st.error("❌ Password baru tidak boleh kosong!")
                elif new_p != conf_p:
                    st.error("❌ Konfirmasi password tidak cocok!")
                else:
                    try:
                        cursor.execute("UPDATE user SET password=%s WHERE username=%s", (new_p, uname))
                        conn.commit()
                        catat_log("Mengubah kata sandi akun")
                        st.success("🔒 Password berhasil diperbarui!")
                    except Exception as e:
                        st.error(f"Error: {e}")


# ---------------------------------------------------------
# 10. HALAMAN INPUT PENILAIAN
# ---------------------------------------------------------
def halaman_input_nilai():
    render_topbar("📝 Input Penilaian")
    render_page_header("📝", "Input Penilaian Aktual Siswa", "Modul Core Engine: Menginput nilai tes untuk diproses pada algoritma Profile Matching")

    cursor.execute("SELECT kd_siswa, nama_siswa FROM siswa ORDER BY nama_siswa ASC")
    data_siswa = cursor.fetchall()
    cursor.execute("SELECT id_kriteria, nama_kriteria FROM kriteria")
    data_kriteria = cursor.fetchall()

    if not data_siswa or not data_kriteria:
        st.warning("⚠️ Data Master belum lengkap. Lengkapi Data Anggota dan Kriteria terlebih dahulu.")
        return

    opsi_siswa = {f"{s['kd_siswa']} - {s['nama_siswa']}": s['kd_siswa'] for s in data_siswa}
    pilih = st.selectbox("🎓 Pilih Siswa yang Dinilai:", list(opsi_siswa.keys()))
    kd_terpilih = opsi_siswa[pilih]

    pilihan_skala = [
        "1 - Sangat Kurang",
        "2 - Kurang",
        "3 - Cukup / Standar",
        "4 - Baik",
        "5 - Sangat Baik"
    ]

    # Tampilkan nilai lama jika ada
    cursor.execute("SELECT id_kriteria, nilai_aktual FROM nilai_siswa WHERE kd_siswa = %s", (kd_terpilih,))
    nilai_lama = {n['id_kriteria']: n['nilai_aktual'] for n in cursor.fetchall()}

    render_divider_arabic()
    st.markdown("""
    <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:16px;margin-bottom:12px;">
        <div style="font-size:13px;font-weight:500;color:#10b981;margin-bottom:4px;">📊 Skala Penilaian</div>
        <div style="font-size:11px;color:#64748b;">1 = Sangat Kurang · 2 = Kurang · 3 = Cukup · 4 = Baik · 5 = Sangat Baik</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_input_nilai"):
        nilai_inputan = {}
        c1, c2 = st.columns(2)
        for i, k in enumerate(data_kriteria):
            default_idx = (nilai_lama.get(k['id_kriteria'], 3) - 1)
            with c1 if i % 2 == 0 else c2:
                nilai_inputan[k['id_kriteria']] = st.selectbox(
                    f"📌 {k['nama_kriteria']}",
                    options=pilihan_skala,
                    index=default_idx,
                )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Simpan Nilai ke Database", type="primary"):
            try:
                cursor.execute("DELETE FROM nilai_siswa WHERE kd_siswa = %s", (kd_terpilih,))
                for id_k, val_str in nilai_inputan.items():
                    angka = int(val_str.split(" - ")[0])
                    cursor.execute(
                        "INSERT INTO nilai_siswa (kd_siswa, id_kriteria, nilai_aktual) VALUES (%s, %s, %s)",
                        (kd_terpilih, id_k, angka)
                    )
                conn.commit()
                catat_log(f"Input/Update nilai siswa ID: {kd_terpilih}")
                st.success("✅ Nilai aktual siswa berhasil disimpan!")
            except Exception as e:
                st.error(f"Kesalahan: {e}")


# ---------------------------------------------------------
# 11. HALAMAN HASIL SPK (PROFILE MATCHING)
# ---------------------------------------------------------
def bobot_gap(gap):
    mapping = {
        0: 5.0, 1: 4.5, -1: 4.0, 2: 3.5, -2: 3.0,
        3: 2.5, -3: 2.0, 4: 1.5, -4: 1.0, 5: 0.5, -5: 0.0
    }
    return mapping.get(gap, 0.0)


def halaman_hasil_spk():
    render_topbar("⭐ Hasil Ranking")
    render_page_header("⭐", "Hasil Ranking Profile Matching", "Rekomendasi penempatan divisi berdasarkan algoritma Profile Matching")

    role_aktif = st.session_state['role'].lower() if st.session_state['logged_in'] else 'publik'

    st.markdown("""
    <div style="background:#0a1e18;border:1px solid #12241f;border-left:4px solid #eab308;border-radius:10px;padding:14px 16px;margin-bottom:14px;">
        <div style="font-size:13px;font-weight:600;color:#eab308;margin-bottom:6px;">📘 Cara Membaca Hasil Rekomendasi</div>
        <div style="font-size:12px;color:#94a3b8;line-height:1.7;">
            Sistem mencocokkan nilai setiap siswa dengan kebutuhan ideal tiap divisi Rohis. Hasil dengan skor tertinggi
            menjadi rekomendasi utama. Istilah <strong>Nilai Kekuatan Utama (NCF)</strong> berarti nilai pada aspek yang paling penting,
            sedangkan <strong>Nilai Pendukung (NSF)</strong> adalah nilai pada aspek pendukung tambahan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    TARGET_DIVISI = {
        "Syiar":             {"K1": 3, "K2": 3, "K3": 4, "K4": 3, "K5": 4},
        "Tilawah (Kesenian)":{"K1": 4, "K2": 4, "K3": 3, "K4": 3, "K5": 4},
        "Da'i (Kesenian)":   {"K1": 3, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "Seni/Kaligrafi":    {"K1": 3, "K2": 3, "K3": 3, "K4": 4, "K5": 4},
        "PSDM":              {"K1": 3, "K2": 3, "K3": 4, "K4": 4, "K5": 4},
        "Sosial":            {"K1": 3, "K2": 3, "K3": 4, "K4": 3, "K5": 4},
        "Takmir Musholla":   {"K1": 4, "K2": 4, "K3": 4, "K4": 3, "K5": 4},
        "CCI (Kesenian)":    {"K1": 4, "K2": 4, "K3": 4, "K4": 4, "K5": 4},
        "Tahfidz (Kesenian)":{"K1": 4, "K2": 4, "K3": 3, "K4": 3, "K5": 4},
    }

    DIVISI_IDS = {
        "Syiar": 1, "Tilawah (Kesenian)": 2, "Da'i (Kesenian)": 3,
        "Seni/Kaligrafi": 4, "PSDM": 5, "Sosial": 6,
        "Takmir Musholla": 7, "CCI (Kesenian)": 8, "Tahfidz (Kesenian)": 9
    }

    def get_data_klasemen():
        cursor.execute("""
            SELECT h.kd_siswa, s.nama_siswa, s.kelas, h.skor_akhir,
                   GROUP_CONCAT(d.nama_divisi SEPARATOR ' / ') as nama_divisi
            FROM hasil_ranking h
            JOIN siswa s ON h.kd_siswa = s.kd_siswa
            JOIN divisi d ON h.id_divisi = d.id_divisi
            GROUP BY h.kd_siswa, s.nama_siswa, s.kelas, h.skor_akhir
        """)
        hasil_db = cursor.fetchall()
        if not hasil_db:
            return []

        data = []
        for row in hasil_db:
            skor_float = float(row['skor_akhir'])
            persen = (skor_float / 5.0) * 100
            div_name = row['nama_divisi'].split(" / ")[0]

            cursor.execute("SELECT id_kriteria, nilai_aktual FROM nilai_siswa WHERE kd_siswa = %s", (row['kd_siswa'],))
            marks = cursor.fetchall()

            ncf_nilai = 0.0
            if div_name in TARGET_DIVISI and marks:
                na = {f"K{m['id_kriteria']}": m['nilai_aktual'] for m in marks}
                if len(na) == 5:
                    ncf_t, ncf_c = 0, 0
                    for k in ["K1","K2","K3","K4","K5"]:
                        t = TARGET_DIVISI[div_name][k]
                        gap = na[k] - t
                        if t >= 4:
                            ncf_t += bobot_gap(gap)
                            ncf_c += 1
                    ncf_nilai = ncf_t / ncf_c if ncf_c > 0 else 0.0

            data.append({
                "Nama Siswa": row['nama_siswa'],
                "Kelas": row['kelas'],
                "NCF": ncf_nilai,
                "Skor (%)": persen,
                "Rekomendasi": row['nama_divisi'],
            })
        data.sort(key=lambda x: (x['NCF'], x['Skor (%)']), reverse=True)
        return data

    def render_tabel_klasemen():
        data_mentah = get_data_klasemen()
        if not data_mentah:
            st.info("Belum ada data hasil perankingan di database.")
            return

        tab_individu, tab_keseluruhan = st.tabs(["👤 Cek Hasil Individu", "📊 Data Keseluruhan"])

        with tab_individu:
            render_divider_arabic()
            st.markdown("<div style='font-size:13px;color:#94a3b8;margin-bottom:10px;'>🔍 Cari namamu untuk melihat detail rekomendasi divisi yang paling cocok.</div>", unsafe_allow_html=True)

            opsi = [f"{d['Nama Siswa']} (Kelas {d['Kelas']})" for d in data_mentah]
            pilih = st.selectbox("Nama Siswa:", opsi, index=None, placeholder="Ketik atau pilih nama...")

            if pilih:
                d = next(x for x in data_mentah if f"{x['Nama Siswa']} (Kelas {x['Kelas']})" == pilih)
                divisi_utama = d['Rekomendasi'].split(" / ")[0]

                st.markdown(f"""
                <div style="
                    background:linear-gradient(135deg,#0a1e18,#0d2b20);
                    border:1px solid #1b4d37;border-top:3px solid #10b981;
                    border-radius:12px;padding:20px;margin:12px 0;
                ">
                    <div style="font-size:20px;margin-bottom:4px;">🎉</div>
                    <div style="font-size:17px;font-weight:600;color:#10b981;margin-bottom:4px;">
                        Selamat, {d['Nama Siswa']}!
                    </div>
                    <div style="font-size:12px;color:#64748b;">Kelas {d['Kelas']}</div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    render_metric_card_custom("Rekomendasi Divisi", divisi_utama, "", "#10b981", "🏷️")
                with c2:
                    render_metric_card_custom("Tingkat Kecocokan", f"{d['Skor (%)']:.2f}%", "Seberapa cocok nilai siswa dengan kebutuhan divisi", "#eab308", "📊")
                with c3:
                    render_metric_card_custom("Kekuatan Utama", f"{d['NCF']:.2f}/5.00", "Nilai aspek paling penting pada divisi ini (NCF)", "#1D9E75", "⭐")

                st.markdown(f"""
                <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:16px;margin-top:12px;">
                    <div style="font-size:13px;font-weight:500;color:#10b981;margin-bottom:8px;">💡 Alasan Rekomendasi</div>
                    <div style="font-size:12px;color:#94a3b8;line-height:1.7;">
                        Sistem membandingkan nilai siswa dengan kebutuhan ideal setiap divisi. Hasil terbaikmu ada pada
                        divisi <strong style="color:#eab308">{divisi_utama}</strong> karena nilai yang kamu miliki paling mendekati
                        kebutuhan divisi tersebut. Tingkat kecocokanmu mencapai
                        <strong style="color:#10b981">{d['Skor (%)']:.2f}%</strong>, artinya potensi dan kemampuanmu dinilai paling sesuai
                        untuk berkontribusi di divisi ini. Semakin kecil selisih nilai dengan kebutuhan divisi,
                        semakin tinggi rekomendasi yang diberikan sistem.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_keseluruhan:
            if 'filter_divisi' not in st.session_state:
                st.session_state['filter_divisi'] = "Semua Divisi"

            list_divisi = ["Semua Divisi","Syiar","Tilawah (Kesenian)","Da'i (Kesenian)",
                           "Seni/Kaligrafi","PSDM","Sosial","Takmir Musholla","CCI (Kesenian)","Tahfidz (Kesenian)"]

            st.markdown("<div style='font-size:13px;color:#94a3b8;margin-bottom:8px;'>🔍 Filter Divisi:</div>", unsafe_allow_html=True)
            for i in range(0, len(list_divisi), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(list_divisi):
                        div = list_divisi[i + j]
                        with cols[j]:
                            btn_type = "primary" if st.session_state['filter_divisi'] == div else "secondary"
                            if st.button(div, type=btn_type, use_container_width=True, key=f"btn_f_{i+j}"):
                                st.session_state['filter_divisi'] = div
                                st.rerun()

            render_divider_arabic()

            data_fil = data_mentah.copy()
            if st.session_state['filter_divisi'] != "Semua Divisi":
                data_fil = [d for d in data_fil if st.session_state['filter_divisi'] in d['Rekomendasi']]

            klasemen = []
            for idx, d in enumerate(data_fil):
                klasemen.append({
                    "Rank": idx + 1,
                    "Nama Siswa": d['Nama Siswa'],
                    "Kelas": d['Kelas'],
                    "Nilai Kekuatan Utama": f"{d['NCF']:.2f}",
                    "Tingkat Kecocokan": f"{d['Skor (%)']:.2f}%",
                    "Rekomendasi Divisi": d['Rekomendasi'],
                })

            if klasemen:
                df_klas = pd.DataFrame(klasemen)
                c_head, c_pdf, c_xls = st.columns([2, 1, 1])
                with c_head:
                    st.markdown("### 🏆 Tabel Rekomendasi", unsafe_allow_html=True)
                    st.caption("Kolom Nilai Kekuatan Utama menunjukkan nilai aspek yang paling penting untuk divisi yang direkomendasikan.")

                import io
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as w:
                    df_klas.to_excel(w, index=False, sheet_name='Klasemen ROHIS')
                with c_xls:
                    st.download_button("📊 Download Excel", data=buf.getvalue(),
                                       file_name=f"Laporan_Rohis_{datetime.date.today()}.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       use_container_width=True, type="primary")
                try:
                    from fpdf import FPDF
                    import tempfile, os

                    class PDF(FPDF):
                        def header(self):
                            self.set_font('Arial','B',12)
                            self.cell(0,10,'Laporan Hasil Penempatan Divisi ROHIS SMPN 87 Jakarta',0,1,'C')
                            if st.session_state['filter_divisi'] != "Semua Divisi":
                                self.set_font('Arial','I',10)
                                self.cell(0,8,f"Kategori: {st.session_state['filter_divisi']}",0,1,'C')
                            self.ln(5)

                    pdf = PDF()
                    pdf.add_page()
                    headers = ["Rank","Nama Siswa","Kelas","Nilai Utama","Tk. Kecocokan","Rekomendasi Divisi"]
                    widths  = [12, 45, 12, 18, 25, 78]
                    pdf.set_font("Arial",'B',9)
                    for h, w in zip(headers, widths):
                        pdf.cell(w, 10, h, 1, 0, 'C')
                    pdf.ln()
                    pdf.set_font("Arial", size=8)
                    for _, row in df_klas.iterrows():
                        pdf.cell(widths[0], 8, str(row['Rank']), 1, 0, 'C')
                        pdf.cell(widths[1], 8, str(row['Nama Siswa'])[:22], 1, 0, 'L')
                        pdf.cell(widths[2], 8, str(row['Kelas']), 1, 0, 'C')
                        pdf.cell(widths[3], 8, str(row['Nilai Kekuatan Utama']), 1, 0, 'C')
                        pdf.cell(widths[4], 8, str(row['Tingkat Kecocokan']), 1, 0, 'C')
                        rek = str(row['Rekomendasi Divisi'])
                        if len(rek) > 45: rek = rek[:42] + "..."
                        pdf.cell(widths[5], 8, rek, 1, 0, 'L')
                        pdf.ln()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        pdf.output(tmp.name)
                        with open(tmp.name, "rb") as f:
                            pdf_bytes = f.read()
                    os.remove(tmp.name)

                    with c_pdf:
                        st.download_button("📄 Download PDF", data=pdf_bytes,
                                           file_name=f"Laporan_Rohis_{datetime.date.today()}.pdf",
                                           mime="application/pdf",
                                           use_container_width=True, type="primary")
                except ImportError:
                    with c_pdf:
                        st.error("Install fpdf: pip install fpdf")

                st.dataframe(df_klas, hide_index=True, use_container_width=True)
            else:
                st.warning(f"Belum ada data untuk divisi: **{st.session_state['filter_divisi']}**")

    # === PEMBINA: ada tab kalkulasi ===
    if role_aktif == 'pembina':
        tab_kalkulasi, tab_klasemen = st.tabs(["🧮 Kalkulasi Nilai", "📊 Klasemen & Rekomendasi"])

        with tab_kalkulasi:
            DATA_TARGET = {
                "Divisi / Peminatan": [
                    "Syiar","Tilawah (Kesenian)","Da'i (Kesenian)","Seni/Kaligrafi",
                    "PSDM","Sosial","Takmir Musholla","CCI (Kesenian)","Tahfidz (Kesenian)"
                ],
                "K1": [3,4,3,3,3,3,4,4,4],
                "K2": [3,4,4,3,3,3,4,4,4],
                "K3": [4,3,4,3,4,4,4,4,3],
                "K4": [3,3,3,4,4,3,3,3,3],
                "K5": [4,4,4,4,4,4,4,4,4],
            }
            df_target = pd.DataFrame(DATA_TARGET)

            cursor.execute("SELECT kd_siswa, nama_siswa FROM siswa")
            data_siswa = cursor.fetchall()

            if not data_siswa:
                st.warning("Belum ada data siswa di database.")
            else:
                opsi = [f"{s['kd_siswa']} - {s['nama_siswa']}" for s in data_siswa]
                pilih = st.selectbox("Pilih siswa untuk melihat proses rekomendasinya:", opsi)
                kd_siswa = int(pilih.split(" - ")[0])

                cursor.execute(
                    "SELECT id_kriteria, nilai_aktual FROM nilai_siswa WHERE kd_siswa = %s ORDER BY id_kriteria ASC",
                    (kd_siswa,)
                )
                data_nilai = cursor.fetchall()

                if len(data_nilai) < 5:
                    st.markdown("""
                    <div style="background:#180a0a;border:1px solid #3b1515;border-left:4px solid #ef4444;
                                border-radius:8px;padding:12px 16px;">
                        <div style="font-size:13px;color:#fca5a5;font-weight:500;">⚠️ Data Nilai Tidak Lengkap</div>
                        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">
                            Siswa ini belum memiliki data nilai pada 5 kriteria. Silakan input penilaian terlebih dahulu.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    nilai_aktual = {f"K{n['id_kriteria']}": n['nilai_aktual'] for n in data_nilai}

                    render_divider_arabic()
                    st.markdown(f"""
                    <div style="background:#0a1e18;border:1px solid #12241f;border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                        <div style="font-size:12px;color:#64748b;margin-bottom:4px;">Nilai Aktual Terdaftar</div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            {"".join([f'<span style="background:#0d2b20;color:#10b981;border:1px solid #1b382e;border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600;">{k}: {v}</span>' for k, v in nilai_aktual.items()])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    df_gap = df_target.copy()
                    kriteria_list = ["K1","K2","K3","K4","K5"]
                    hasil_perh = []

                    for i, row in df_gap.iterrows():
                        ncf_t, ncf_c = 0, 0
                        nsf_t, nsf_c = 0, 0
                        for k in kriteria_list:
                            target = df_target.loc[i, k]
                            aktual = nilai_aktual[k]
                            gap = aktual - target
                            df_gap.loc[i, k] = gap
                            b = bobot_gap(gap)
                            if target >= 4:
                                ncf_t += b; ncf_c += 1
                            elif target == 3:
                                nsf_t += b; nsf_c += 1
                        ncf = ncf_t / ncf_c if ncf_c > 0 else 0
                        nsf = nsf_t / nsf_c if nsf_c > 0 else 0
                        hasil_perh.append({
                            'Divisi / Peminatan': row['Divisi / Peminatan'],
                            'NCF': ncf, 'NSF': nsf,
                            'Skor Akhir': (0.6 * ncf) + (0.4 * nsf)
                        })

                    def color_gap(val):
                        if isinstance(val, int):
                            if val == 0: return 'color: #10b981; font-weight: bold;'
                            elif val > 0: return 'color: #38bdf8;'
                            elif val < 0: return 'color: #ef4444;'
                        return ''

                    st.markdown("""
                    <div style="background:#0a1e18;border:1px solid #12241f;border-radius:10px;padding:14px 16px;margin-top:10px;">
                        <div style="font-size:13px;font-weight:600;color:#10b981;margin-bottom:6px;">ℹ️ Penjelasan Singkat Perhitungan</div>
                        <div style="font-size:12px;color:#94a3b8;line-height:1.7;">
                            <strong>Selisih Nilai</strong> menunjukkan perbedaan antara nilai siswa dan kebutuhan tiap divisi.<br>
                            <strong>Nilai Kekuatan Utama (NCF)</strong> adalah rata-rata aspek yang paling penting pada divisi.<br>
                            <strong>Nilai Pendukung (NSF)</strong> adalah rata-rata aspek pendukung tambahan.<br>
                            <strong>Skor Rekomendasi</strong> dihitung dari gabungan NCF 60% dan NSF 40%.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    tampil_detail = st.checkbox("Tampilkan detail perbandingan nilai dan hasil rekomendasi", key=f"detail_hasil_{kd_siswa}")
                    if tampil_detail:
                        st.markdown("### 1. Perbandingan Nilai Siswa dengan Kebutuhan Divisi")
                        st.caption("Angka pada tabel menunjukkan selisih antara nilai siswa dan standar yang dibutuhkan tiap divisi. Nilai 0 berarti sangat sesuai.")
                        st.dataframe(df_gap.style.map(color_gap, subset=kriteria_list), hide_index=True, use_container_width=True)
                        df_hasil = pd.DataFrame(hasil_perh).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)
                        df_hasil = df_hasil.rename(columns={
                            'NCF': 'Nilai Kekuatan Utama (NCF)',
                            'NSF': 'Nilai Pendukung (NSF)',
                            'Skor Akhir': 'Skor Rekomendasi'
                        })
                        st.markdown("### 2. Hasil Nilai Utama, Pendukung, dan Skor Rekomendasi")
                        st.caption("Semakin besar skor rekomendasi, semakin cocok siswa ditempatkan pada divisi tersebut.")
                        st.dataframe(df_hasil, hide_index=True, use_container_width=True)

                    render_divider_arabic()
                    if st.button("💾 Simpan Rekomendasi ke Klasemen", type="primary"):
                        try:
                            df_hasil2 = pd.DataFrame(hasil_perh).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)
                            max_skor = df_hasil2['Skor Akhir'].max()
                            top = df_hasil2[df_hasil2['Skor Akhir'] == max_skor]

                            cursor.execute("DELETE FROM hasil_ranking WHERE kd_siswa = %s", (kd_siswa,))
                            saved = []
                            for _, row in top.iterrows():
                                id_div = DIVISI_IDS.get(row['Divisi / Peminatan'])
                                if id_div:
                                    cursor.execute(
                                        "INSERT INTO hasil_ranking (kd_siswa, id_divisi, skor_akhir) VALUES (%s, %s, %s)",
                                        (kd_siswa, id_div, float(row['Skor Akhir']))
                                    )
                                    saved.append(row['Divisi / Peminatan'])
                            conn.commit()
                            nama_div = " / ".join(saved)
                            catat_log(f"Menyimpan hasil ranking ({nama_div}) untuk siswa ID: {kd_siswa}")
                            st.success(f"✅ Berhasil menyimpan rekomendasi divisi **{nama_div}**! Cek Tab Klasemen.")
                        except Exception as e:
                            st.error(f"Kesalahan: {e}")

        with tab_klasemen:
            render_tabel_klasemen()

    else:
        render_tabel_klasemen()


# ---------------------------------------------------------
# 12. ROUTING UTAMA & SIDEBAR
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    # Tombol login di pojok kanan atas
    c_kiri, c_kanan = st.columns([8, 1])
    with c_kanan:
        if st.session_state['menu_aktif'] != "Login Akses":
            if st.button("Login 👤", type="primary", use_container_width=True):
                st.session_state['menu_aktif'] = "Login Akses"
                st.rerun()
        else:
            if st.button("← Kembali", use_container_width=True):
                st.session_state['menu_aktif'] = "🏠 Dashboard"
                st.rerun()

    with st.sidebar:
        render_sidebar_logo()

        if st.session_state['menu_aktif'] != "Login Akses":
            st.markdown("<div style='padding:6px 4px 6px;font-size:10px;color:#3d6b5a;text-transform:uppercase;letter-spacing:1.5px;margin-top:8px;'>Menu Publik</div>", unsafe_allow_html=True)
            render_sidebar_menu(["🏠 Dashboard", "⭐ Hasil Ranking"], key_prefix="public_menu")
            st.divider()
            render_sidebar_access_note("public")
        else:
            render_sidebar_access_note("login")

    # Render halaman
    page = st.session_state['menu_aktif']
    if page == "🏠 Dashboard":
        halaman_dashboard()
    elif page == "⭐ Hasil Ranking":
        halaman_hasil_spk()
    elif page == "Login Akses":
        halaman_login()

else:
    # Tombol logout
    c_kiri, c_kanan = st.columns([8, 1])
    with c_kanan:
        if st.button("Keluar 🚪", use_container_width=True):
            dialog_konfirmasi_logout()

    with st.sidebar:
        render_sidebar_logo()

        role_aktif = st.session_state['role'].lower()
        username = st.session_state['username']

        if role_aktif == 'pengurus':
            daftar_menu = ["🏠 Dashboard", "👥 Data Anggota", "⭐ Hasil Ranking", "⚙️ Pengaturan"]
        elif role_aktif == 'pembina':
            daftar_menu = ["🏠 Dashboard", "📝 Input Penilaian", "⭐ Hasil Ranking", "⚙️ Pengaturan"]
        else:
            daftar_menu = ["🏠 Dashboard", "⚙️ Pengaturan"]

        st.markdown("<div style='padding:6px 4px 6px;font-size:10px;color:#3d6b5a;text-transform:uppercase;letter-spacing:1.5px;margin-top:8px;'>Menu Utama</div>", unsafe_allow_html=True)
        render_sidebar_menu(daftar_menu, key_prefix="main_menu")
        menu_pilihan = st.session_state.get('menu_aktif') or daftar_menu[0]
        if menu_pilihan not in daftar_menu:
            menu_pilihan = daftar_menu[0]
            st.session_state['menu_aktif'] = menu_pilihan

        st.divider()
        render_sidebar_user_card(username, role_aktif)

    if menu_pilihan == "🏠 Dashboard":
        halaman_dashboard()
    elif menu_pilihan == "👥 Data Anggota":
        halaman_data_siswa()
    elif menu_pilihan == "📝 Input Penilaian":
        halaman_input_nilai()
    elif menu_pilihan == "⭐ Hasil Ranking":
        halaman_hasil_spk()
    elif menu_pilihan == "⚙️ Pengaturan":
        halaman_profil()

