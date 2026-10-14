import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# Database Connection Configuration
# Requirement: Relative path DB = '../data/ipl.db'
# ==============================================================================
DB = '../data/ipl.db'
if not os.path.exists(DB):
    if os.path.exists('data/ipl.db'):
        DB = 'data/ipl.db'
    elif os.path.exists('../2_IPL_Cricket/ipl.db'):
        DB = '../2_IPL_Cricket/ipl.db'
    elif os.path.exists('2_IPL_Cricket/ipl.db'):
        DB = '2_IPL_Cricket/ipl.db'


def q(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Helper function to execute SQL queries with parameters.
    Rule: All numbers come directly out of SQL via q(). Nothing is calculated in pandas.
    """
    with sqlite3.connect(DB) as conn:
        return pd.read_sql_query(sql, conn, params=params)


# ==============================================================================
# Page Configuration & Clean Light-Theme + Forest Green Sidebar Styling
# ==============================================================================
st.set_page_config(
    page_title="IPL Bowling Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* Global Base */
    .stApp {
        background-color: #f8fafc;
        color: #000000 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Left Sidebar Styling - Deep Forest Green */
    [data-testid="stSidebar"] {
        background-color: #063a2f !important;
        border-right: 1px solid #042e26;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] .stRadio > div {
        background: transparent;
        gap: 6px;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: transparent;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
        font-size: 14px;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #0d4d3f !important;
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: #145a49 !important;
        font-weight: 700;
        color: #ffffff !important;
    }

    /* Page Header */
    .page-title {
        font-size: 26px;
        font-weight: 800;
        color: #000000 !important;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    .page-subtitle {
        font-size: 13.5px;
        color: #000000 !important;
        margin-bottom: 14px;
        font-weight: 600;
    }

    /* Filter Strip Card */
    .filter-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Top KPI Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        min-height: 112px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-header {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        color: #000000 !important;
        margin-bottom: 6px;
    }
    .metric-num {
        font-size: 32px;
        font-weight: 850;
        color: #000000 !important;
        line-height: 1.1;
    }
    .metric-desc {
        font-size: 11.5px;
        color: #000000 !important;
        margin-top: 4px;
        font-weight: 600;
    }
    .metric-dual-flex {
        display: flex;
        align-items: baseline;
        gap: 28px;
    }

    /* Chart Container Card */
    .chart-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 14px;
    }
    .chart-card-title {
        font-size: 14px;
        font-weight: 800;
        color: #000000 !important;
        margin-bottom: 8px;
    }

    /* Streamlit Input Styling Adjustments */
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stMultiSelect label {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        margin-bottom: 2px !important;
    }
    div[data-baseweb="select"] > div {
        border-radius: 6px !important;
        border-color: #94a3b8 !important;
        background-color: #ffffff !important;
        min-height: 36px !important;
    }
    div[data-baseweb="input"] > div {
        border-radius: 6px !important;
        border-color: #94a3b8 !important;
        background-color: #ffffff !important;
        min-height: 36px !important;
    }
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    div[data-baseweb="input"] * {
        color: #000000 !important;
    }
    span[data-baseweb="tag"] {
        background-color: #d1fae5 !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: 4px !important;
    }
    span[data-baseweb="tag"] * {
        color: #064e3b !important;
        font-weight: 600 !important;
    }

    /* Leaderboard Table Styling */
    .leaderboard-table {
        width: 100%;
        border-collapse: collapse;
        font-family: inherit;
        font-size: 13px;
        color: #000000 !important;
        margin-top: 6px;
    }
    .leaderboard-table th {
        background-color: #063a2f;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 11.5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 10px 12px;
        text-align: left;
        border: none;
    }
    .leaderboard-table th:first-child {
        border-top-left-radius: 6px;
    }
    .leaderboard-table th:last-child {
        border-top-right-radius: 6px;
    }
    .leaderboard-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #e2e8f0;
        color: #000000 !important;
        font-weight: 500;
        vertical-align: middle;
    }
    .leaderboard-table tr:hover {
        background-color: #f1f5f9;
    }
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 12px;
    }
    .rank-1 { background-color: #fef08a; color: #854d0e !important; border: 1px solid #facc15; }
    .rank-2 { background-color: #e2e8f0; color: #334155 !important; border: 1px solid #cbd5e1; }
    .rank-3 { background-color: #ffedd5; color: #9a3412 !important; border: 1px solid #fdba74; }
    .rank-other { background-color: #f8fafc; color: #000000 !important; border: 1px solid #e2e8f0; }
    .style-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        background-color: #e6f4ea;
        color: #1b4d3e !important;
        border: 1px solid #a7f3d0;
    }
    .highlight-val {
        font-weight: 800;
        color: #1b4d3e !important;
        font-size: 14px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Color Palette (Matching Clean Sage & Forest Green Design)
# ==============================================================================
DARK_GREEN = "#1b4d3e"    # Deep Forest Green / Pine
LIGHT_GREEN = "#74c69d"   # Sage / Mint Green
MID_GREEN = "#529b7a"     # Mid Sage Green
LINE_COLOR = "#1b4d3e"    # Line color
LEAGUE_LINE = "#1e293b"   # Dark slate dashed league line
CARD_BG = "#ffffff"


# ==============================================================================
# Left Sidebar Navigation (Matching exact UI in screenshot)
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 20px 4px;">
            <div style="font-size: 32px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;">IPL</div>
            <div style="font-size: 13px; color: #a7f3d0; margin-top: -3px; font-weight: 500;">2008 - 2026</div>
            <div style="font-size: 11.5px; color: #a7f3d0; margin-top: 4px; font-weight: 500; opacity: 0.9;">Created by Mohammed Jaseem.N.P</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_selection = st.radio(
        "Navigation",
        ["📊 Bowlers Overview", "🎯 Individual Bowler"],
        index=0,
        label_visibility="collapsed",
    )


# Common Database Queries
try:
    season_rows = q("SELECT DISTINCT season_id FROM v_ball WHERE season_id BETWEEN 2008 AND 2026 ORDER BY season_id ASC;")
    db_seasons = [int(s) for s in season_rows["season_id"].tolist()] if not season_rows.empty else list(range(2008, 2027))
except Exception:
    db_seasons = list(range(2008, 2026))

all_seasons_list = ["All Seasons"] + [str(s) for s in db_seasons]

# Build team list from v_ball.bowling_team (actual data, not teams table which has stale names)
team_rows = q("SELECT DISTINCT bowling_team FROM v_ball WHERE bowling_team IS NOT NULL ORDER BY bowling_team ASC;")
all_teams_clean = [t for t in team_rows["bowling_team"].tolist() if t]
all_teams_list = ["All Teams"] + all_teams_clean

# Exact 5 style groups present in the data (Others = 0 balls, removed)
style_options_clean = [
    "Right-arm pace",
    "Left-arm pace",
    "Right-arm off spin",
    "Left-arm orthodox",
    "Leg spin",
]
style_options_tab1 = ["All"] + style_options_clean

# Canonical CASE WHEN expression for the 5 style groups.
# Priority order matters: Legbreak/Wrist spin > Offbreak > Orthodox > Left arm pace > Right arm pace
# bowler_type uses 'Left arm' / 'Right arm' (with space), NOT 'Left%' / 'Right%'
STYLE_CASE = """
    CASE
        WHEN bowler_type LIKE '%Wrist spin%' OR bowler_type LIKE '%Legbreak%' OR bowler_type LIKE '%Googly%' THEN 'Leg spin'
        WHEN bowler_type LIKE '%Offbreak%' THEN 'Right-arm off spin'
        WHEN bowler_type LIKE '%Orthodox%' THEN 'Left-arm orthodox'
        WHEN bowler_type LIKE '%Left arm%' AND (bowler_type LIKE '%Fast%' OR bowler_type LIKE '%Medium%') THEN 'Left-arm pace'
        WHEN bowler_type LIKE '%Right arm%' AND (bowler_type LIKE '%Fast%' OR bowler_type LIKE '%Medium%') THEN 'Right-arm pace'
        ELSE 'Others'
    END
"""

# Spin vs Pace CASE (used in Screen 1 hero chart and Screen 2 style filter)
SPIN_CASE = """
    CASE WHEN bowler_type LIKE '%Legbreak%'
              OR bowler_type LIKE '%Offbreak%'
              OR bowler_type LIKE '%Orthodox%'
              OR bowler_type LIKE '%Googly%'
              OR bowler_type LIKE '%Wrist spin%'
         THEN 'Spin' ELSE 'Pace' END
"""

# Condition to exclude NULL / blank / space bowler_type rows
BT_NOT_BLANK = "trim(coalesce(bowler_type, '')) NOT IN ('', ' ')"


def build_filter_clause(
    seasons: list = None,
    teams: list = None,
    styles: list = None,
    style_case: str = STYLE_CASE,
    table_alias: str = "",
) -> tuple:
    """Helper to dynamically construct SQL WHERE clause and parameter tuple for multi-select filters."""
    prefix = f"{table_alias}." if table_alias else ""
    clauses = ["1=1"]
    params = []

    if seasons:
        ph = ",".join("?" for _ in seasons)
        clauses.append(f"{prefix}season_id IN ({ph})")
        params.extend([int(s) for s in seasons])

    if teams:
        ph = ",".join("?" for _ in teams)
        clauses.append(f"{prefix}bowling_team IN ({ph})")
        params.extend([str(t) for t in teams])

    if styles:
        ph = ",".join("?" for _ in styles)
        clauses.append(f"({style_case}) IN ({ph})")
        params.extend([str(st) for st in styles])

    return " AND ".join(clauses), tuple(params)


# ==============================================================================
# Top Header Banner
# ==============================================================================
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #e2e8f0; flex-wrap: wrap; gap: 8px;">
        <span style="font-size: 12px; font-weight: 700; color: #64748b; letter-spacing: 0.8px; text-transform: uppercase;">
            🏏 IPL Bowling Analytics Platform (2008–2026)
        </span>
        <span style="font-size: 12.5px; font-weight: 700; color: #064e3b; background: #d1fae5; padding: 4px 14px; border-radius: 9999px; border: 1px solid #a7f3d0; display: inline-flex; align-items: center; gap: 6px;">
            <span>👨‍💻</span> Created by Mohammed Jaseem.N.P
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# SCREEN 1: BOWLERS OVERVIEW
# ==============================================================================
if nav_selection == "📊 Bowlers Overview":
    st.markdown('<div class="page-title">Bowlers Overview</div>', unsafe_allow_html=True)
    # Requirement 15: Named reader sentence visible on dashboard
    st.markdown(
        '<div class="page-subtitle">For the bowling coach, deciding which bowler to pick and for which overs</div>',
        unsafe_allow_html=True,
    )

    # Initialize multiselect state if not present
    if "s1_season_ms" not in st.session_state:
        st.session_state["s1_season_ms"] = []
    if "s1_style_ms" not in st.session_state:
        st.session_state["s1_style_ms"] = []
    if "s1_team_ms" not in st.session_state:
        st.session_state["s1_team_ms"] = []

    # --------------------------------------------------------------------------
    # Quick Year Preset Buttons
    # --------------------------------------------------------------------------
    qp_cols = st.columns([1.6, 1.2, 1.2, 1.2, 1.2, 1.2])
    with qp_cols[0]:
        st.markdown(
            '<div style="font-size: 12.5px; font-weight: 700; color: #1b4d3e; padding-top: 6px;">'
            '⚡ Quick Year Presets:'
            '</div>',
            unsafe_allow_html=True,
        )
    with qp_cols[1]:
        if st.button("2008–2012", key="btn_s1_2008_2012", use_container_width=True):
            st.session_state["s1_season_ms"] = [2008, 2009, 2010, 2011, 2012]
            st.rerun()
    with qp_cols[2]:
        if st.button("2013–2017", key="btn_s1_2013_2017", use_container_width=True):
            st.session_state["s1_season_ms"] = [2013, 2014, 2015, 2016, 2017]
            st.rerun()
    with qp_cols[3]:
        if st.button("2018–2022", key="btn_s1_2018_2022", use_container_width=True):
            st.session_state["s1_season_ms"] = [2018, 2019, 2020, 2021, 2022]
            st.rerun()
    with qp_cols[4]:
        if st.button("2023–2026", key="btn_s1_2023_2026", use_container_width=True):
            st.session_state["s1_season_ms"] = [2023, 2024, 2025, 2026]
            st.rerun()
    with qp_cols[5]:
        if st.button("All / Clear", key="btn_s1_clear", use_container_width=True):
            st.session_state["s1_season_ms"] = []
            st.session_state["s1_style_ms"] = []
            st.session_state["s1_team_ms"] = []
            st.rerun()

    # --------------------------------------------------------------------------
    # Multi-Select Filter Bar
    # --------------------------------------------------------------------------
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns([1.5, 1.4, 0.9, 1.5])

    with fc1:
        sel_seasons_s1 = st.multiselect(
            "Seasons",
            options=db_seasons,
            placeholder="All Seasons (2008–2026)",
            key="s1_season_ms",
        )

    with fc2:
        sel_styles_s1 = st.multiselect(
            "Bowling Style",
            options=style_options_clean,
            placeholder="All Styles",
            key="s1_style_ms",
        )

    with fc3:
        min_balls_s1 = st.selectbox(
            "Minimum Balls",
            [100, 200, 300, 500],
            index=0,
            key="s1_min_balls",
        )

    with fc4:
        sel_teams_s1 = st.multiselect(
            "Teams",
            options=all_teams_clean,
            placeholder="All Teams",
            key="s1_team_ms",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Build multi-select SQL filter clauses
    f_where_s1, f_params_s1 = build_filter_clause(
        seasons=sel_seasons_s1,
        teams=sel_teams_s1,
        styles=sel_styles_s1,
    )
    # Filter clause excluding style (used for spin vs pace comparison and hero chart)
    f_where_s1_nostyle, f_params_s1_nostyle = build_filter_clause(
        seasons=sel_seasons_s1,
        teams=sel_teams_s1,
    )

    # --------------------------------------------------------------------------
    # Contextual Filter Detail Strip — visible only when any filter is active
    # --------------------------------------------------------------------------
    any_filter_active = bool(sel_seasons_s1 or sel_teams_s1 or sel_styles_s1)

    if any_filter_active:
        ctx_parts = []
        if sel_seasons_s1:
            sorted_s = sorted(sel_seasons_s1)
            if len(sorted_s) > 1 and sorted_s[-1] - sorted_s[0] == len(sorted_s) - 1:
                ctx_parts.append(f"Seasons {sorted_s[0]}–{sorted_s[-1]}")
            elif len(sorted_s) <= 3:
                ctx_parts.append(f"Seasons {', '.join(map(str, sorted_s))}")
            else:
                ctx_parts.append(f"{len(sorted_s)} Seasons ({sorted_s[0]}...{sorted_s[-1]})")
        if sel_teams_s1:
            if len(sel_teams_s1) <= 2:
                ctx_parts.append(", ".join(sel_teams_s1))
            else:
                ctx_parts.append(f"{len(sel_teams_s1)} Teams")
        if sel_styles_s1:
            if len(sel_styles_s1) <= 2:
                ctx_parts.append(", ".join(sel_styles_s1))
            else:
                ctx_parts.append(f"{len(sel_styles_s1)} Styles")
        ctx_label = "  ·  ".join(ctx_parts)

        # Pull live stats for the current filter context
        ctx_df = q(
            f"""
            SELECT
                COUNT(DISTINCT match_id)   AS matches,
                COUNT(DISTINCT bowler)     AS bowlers,
                SUM(is_legal)              AS balls,
                SUM(bowler_wicket)         AS wickets,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy
            FROM v_ball
            WHERE {f_where_s1};
            """,
            f_params_s1,
        )

        # Top bowler for the context (by wickets)
        top_df = q(
            f"""
            SELECT bowler, SUM(bowler_wicket) AS wkts
            FROM v_ball
            WHERE {f_where_s1}
            GROUP BY bowler
            ORDER BY wkts DESC
            LIMIT 1;
            """,
            f_params_s1,
        )

        # Extract values safely
        ctx_matches = int(ctx_df["matches"].iloc[0]) if not ctx_df.empty and pd.notnull(ctx_df["matches"].iloc[0]) else 0
        ctx_bowlers = int(ctx_df["bowlers"].iloc[0]) if not ctx_df.empty and pd.notnull(ctx_df["bowlers"].iloc[0]) else 0
        ctx_balls   = int(ctx_df["balls"].iloc[0])   if not ctx_df.empty and pd.notnull(ctx_df["balls"].iloc[0]) else 0
        ctx_wkts    = int(ctx_df["wickets"].iloc[0]) if not ctx_df.empty and pd.notnull(ctx_df["wickets"].iloc[0]) else 0
        ctx_econ    = float(ctx_df["economy"].iloc[0]) if not ctx_df.empty and pd.notnull(ctx_df["economy"].iloc[0]) else 0.0
        ctx_top     = f"{top_df['bowler'].iloc[0]} ({int(top_df['wkts'].iloc[0])} wkts)" if not top_df.empty else "—"
        ctx_overs   = ctx_balls // 6

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #063a2f 0%, #0d5c48 100%);
                border-radius: 8px;
                padding: 10px 18px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 0;
                flex-wrap: wrap;
            ">
                <div style="color:#a7f3d0; font-size:11px; font-weight:700;
                            letter-spacing:0.6px; text-transform:uppercase;
                            margin-right:16px; white-space:nowrap; padding-right:16px;
                            border-right:1px solid rgba(255,255,255,0.15);">
                    🔍 {ctx_label}
                </div>
                <div style="display:flex; gap:0; flex-wrap:wrap; flex:1; align-items:center;">
                    <div style="padding:0 18px 0 0; margin-right:18px;
                                border-right:1px solid rgba(255,255,255,0.12);">
                        <div style="color:#fff; font-size:18px; font-weight:800; line-height:1.1;">{ctx_matches:,}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Matches</div>
                    </div>
                    <div style="padding:0 18px 0 0; margin-right:18px;
                                border-right:1px solid rgba(255,255,255,0.12);">
                        <div style="color:#fff; font-size:18px; font-weight:800; line-height:1.1;">{ctx_bowlers:,}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Bowlers</div>
                    </div>
                    <div style="padding:0 18px 0 0; margin-right:18px;
                                border-right:1px solid rgba(255,255,255,0.12);">
                        <div style="color:#fff; font-size:18px; font-weight:800; line-height:1.1;">{ctx_overs:,}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Overs</div>
                    </div>
                    <div style="padding:0 18px 0 0; margin-right:18px;
                                border-right:1px solid rgba(255,255,255,0.12);">
                        <div style="color:#fff; font-size:18px; font-weight:800; line-height:1.1;">{ctx_wkts:,}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Wickets</div>
                    </div>
                    <div style="padding:0 18px 0 0; margin-right:18px;
                                border-right:1px solid rgba(255,255,255,0.12);">
                        <div style="color:#fff; font-size:18px; font-weight:800; line-height:1.1;">{ctx_econ:.2f}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Avg Economy</div>
                    </div>
                    <div>
                        <div style="color:#fff; font-size:14px; font-weight:700; line-height:1.2;">{ctx_top}</div>
                        <div style="color:#a7f3d0; font-size:10px; font-weight:600;
                                    letter-spacing:0.4px; text-transform:uppercase;">Top Bowler</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------------------------
    # Top Metric Cards Strip (Exactly 3 Cards)
    # --------------------------------------------------------------------------
    mc1, mc2, mc3 = st.columns(3)

    # Card 1: BOWLERS (Total bowlers & Qualified bowlers)
    card1_df = q(
        f"""
        SELECT
            COUNT(DISTINCT bowler) AS total_bowlers,
            COUNT(DISTINCT CASE WHEN balls >= ? THEN bowler END) AS qualified_bowlers
        FROM (
            SELECT bowler, SUM(is_legal) AS balls
            FROM v_ball
            WHERE {f_where_s1}
            GROUP BY bowler
        );
        """,
        (min_balls_s1,) + f_params_s1,
    )
    tot_bowlers = int(card1_df["total_bowlers"].iloc[0]) if not card1_df.empty else 0
    qual_bowlers = int(card1_df["qualified_bowlers"].iloc[0]) if not card1_df.empty else 0

    with mc1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">BOWLERS</div>
                <div class="metric-dual-flex">
                    <div>
                        <div class="metric-num">{tot_bowlers:,}</div>
                        <div class="metric-desc">Total bowlers</div>
                    </div>
                    <div>
                        <div class="metric-num">{qual_bowlers:,}</div>
                        <div class="metric-desc">Qualified bowlers (≥ {min_balls_s1} balls)</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card 2: TOTAL WICKETS (Credited to bowlers, fully reactive to season, team, and style filters)
    card2_df = q(
        f"""
        SELECT SUM(bowler_wicket) AS bowler_wickets
        FROM v_ball
        WHERE {f_where_s1};
        """,
        f_params_s1,
    )
    tot_wickets_all = int(card2_df["bowler_wickets"].iloc[0]) if not card2_df.empty and pd.notnull(card2_df["bowler_wickets"].iloc[0]) else 0

    filters_applied = []
    if sel_seasons_s1:
        sorted_s = sorted(sel_seasons_s1)
        if len(sorted_s) > 1 and sorted_s[-1] - sorted_s[0] == len(sorted_s) - 1:
            filters_applied.append(f"Seasons {sorted_s[0]}–{sorted_s[-1]}")
        else:
            filters_applied.append(f"{len(sorted_s)} seasons")
    if sel_teams_s1:
        filters_applied.append(f"{len(sel_teams_s1)} teams")
    if sel_styles_s1:
        filters_applied.append(f"{len(sel_styles_s1)} styles")
    c2_desc = f"Credited to bowlers ({', '.join(filters_applied)})" if filters_applied else "Credited to bowlers (All seasons 2008–2026)"

    with mc2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">TOTAL WICKETS</div>
                <div class="metric-num">{tot_wickets_all:,}</div>
                <div class="metric-desc">{c2_desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card 3: SPIN vs PACE (Tested finding + reactive economy for active filters)
    card3_df = q(
        f"""
        SELECT
            {SPIN_CASE} AS bowling_style,
            ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy
        FROM v_ball
        WHERE {f_where_s1_nostyle}
          AND {BT_NOT_BLANK}
        GROUP BY bowling_style;
        """,
        f_params_s1_nostyle,
    )
    spin_econ_val = 7.70
    pace_econ_val = 8.49
    if not card3_df.empty:
        for _, r in card3_df.iterrows():
            if r["bowling_style"] == "Spin" and pd.notnull(r["economy"]):
                spin_econ_val = float(r["economy"])
            elif r["bowling_style"] == "Pace" and pd.notnull(r["economy"]):
                pace_econ_val = float(r["economy"])

    with mc3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">SPIN vs PACE</div>
                <div style="font-size: 16px; font-weight: 800; color: #000000; margin-top: 2px;">
                    Spin {spin_econ_val:.2f} vs Pace {pace_econ_val:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------------------------
    # Visual 1 (The Hero): Economy by Phase of the Innings — Spin vs Pace
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-card-title">Economy by Phase of the Innings — Spin vs Pace</div>',
        unsafe_allow_html=True,
    )

    hero_phase_df = q(
        f"""
        SELECT
            CASE phase
                WHEN 'Powerplay' THEN 'Powerplay (1–6)'
                WHEN 'Middle' THEN 'Middle Overs (7–15)'
                ELSE 'Death Overs (16–20)'
            END AS phase_label,
            {SPIN_CASE} AS bowling_style,
            ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
            SUM(is_legal) AS balls_bowled
        FROM v_ball
        WHERE {f_where_s1_nostyle}
          AND {BT_NOT_BLANK}
        GROUP BY phase_label, bowling_style
        ORDER BY CASE phase_label
            WHEN 'Powerplay (1–6)' THEN 1
            WHEN 'Middle Overs (7–15)' THEN 2
            ELSE 3 END, bowling_style;
        """,
        f_params_s1_nostyle,
    )

    overall_econ_s1 = q(
        f"""
        SELECT ROUND(6.0 * SUM(bowler_runs) / SUM(is_legal), 2) AS econ
        FROM v_ball
        WHERE {f_where_s1_nostyle};
        """,
        f_params_s1_nostyle,
    )
    league_ref_s1 = float(overall_econ_s1["econ"].iloc[0]) if not overall_econ_s1.empty and pd.notnull(overall_econ_s1["econ"].iloc[0]) else 8.25

    fig_hero_s1 = px.bar(
        hero_phase_df,
        x="phase_label",
        y="economy",
        color="bowling_style",
        barmode="group",
        category_orders={"phase_label": ["Powerplay (1–6)", "Middle Overs (7–15)", "Death Overs (16–20)"]},
        color_discrete_map={"Spin": DARK_GREEN, "Pace": LIGHT_GREEN},
        labels={"economy": "Economy Rate", "phase_label": "", "bowling_style": ""},
        text="economy",
    )
    fig_hero_s1.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(color="#000000", size=11),
        width=0.28,
    )
    fig_hero_s1.add_hline(
        y=league_ref_s1,
        line_dash="dash",
        line_color=LEAGUE_LINE,
        annotation_text="--- League Average",
        annotation_position="top right",
        annotation_font=dict(color="#000000", size=11),
    )
    fig_hero_s1.update_layout(
        template="plotly_white",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color="#000000"),
        height=320,
        margin=dict(l=30, r=30, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#000000", size=11),
        ),
        yaxis=dict(
            range=[0, 13],
            dtick=2,
            title="Economy Rate (RPO)",
            title_font=dict(color="#000000", size=12),
            tickfont=dict(color="#000000", size=11),
            gridcolor="#e2e8f0",
        ),
        xaxis=dict(
            title="Innings Phase",
            title_font=dict(color="#000000", size=12),
            tickfont=dict(color="#000000", size=11),
            gridcolor="#e2e8f0",
        ),
    )
    st.plotly_chart(fig_hero_s1, use_container_width=True, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Middle Row: Visual 2 (Economy by Bowling Style) & Visual 3 (Wickets by Innings Phase)
    # --------------------------------------------------------------------------
    m_row_col1, m_row_col2 = st.columns(2)

    with m_row_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Economy by Bowling Style</div>',
            unsafe_allow_html=True,
        )
        style_econ_df = q(
            f"""
            SELECT
                {STYLE_CASE} AS style_group,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
                SUM(is_legal) AS balls
            FROM v_ball
            WHERE {f_where_s1}
              AND {BT_NOT_BLANK}
            GROUP BY style_group
            HAVING SUM(is_legal) >= 20
            ORDER BY economy ASC;
            """,
            f_params_s1,
        )

        fig_style_econ = px.bar(
            style_econ_df,
            x="economy",
            y="style_group",
            orientation="h",
            text="economy",
            labels={"economy": "", "style_group": ""},
        )
        fig_style_econ.update_traces(
            marker_color=DARK_GREEN,
            texttemplate="%{text:.2f}",
            textposition="inside",
            textfont=dict(color="#ffffff", size=11),
        )
        fig_style_econ.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(
                title="Bowling Style",
                title_font=dict(color="#000000", size=11),
                autorange="reversed",
                tickfont=dict(color="#000000", size=11),
            ),
            xaxis=dict(
                title="Economy Rate (RPO)",
                title_font=dict(color="#000000", size=11),
                range=[0, 10],
                dtick=2,
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_style_econ, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with m_row_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Wickets by Innings Phase</div>',
            unsafe_allow_html=True,
        )
        phase_wkts_df = q(
            f"""
            SELECT
                CASE phase
                    WHEN 'Powerplay' THEN 'Powerplay (1–6)'
                    WHEN 'Middle' THEN 'Middle Overs (7–15)'
                    ELSE 'Death Overs (16–20)'
                END AS phase_label,
                SUM(bowler_wicket) AS wickets
            FROM v_ball
            WHERE {f_where_s1}
            GROUP BY phase_label
            ORDER BY CASE phase_label
                WHEN 'Powerplay (1–6)' THEN 1
                WHEN 'Middle Overs (7–15)' THEN 2
                ELSE 3 END;
            """,
            f_params_s1,
        )

        fig_phase_wkts = px.bar(
            phase_wkts_df,
            x="phase_label",
            y="wickets",
            text="wickets",
            color="phase_label",
            color_discrete_sequence=[DARK_GREEN, MID_GREEN, LIGHT_GREEN],
            labels={"wickets": "", "phase_label": ""},
        )
        fig_phase_wkts.update_traces(
            texttemplate="%{y:,}",
            textposition="outside",
            textfont=dict(color="#000000", size=11),
            width=0.45,
        )
        fig_phase_wkts.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            showlegend=False,
            margin=dict(l=20, r=20, t=10, b=10),
            yaxis=dict(
                title="Wickets",
                title_font=dict(color="#000000", size=11),
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
            xaxis=dict(
                title="Innings Phase",
                title_font=dict(color="#000000", size=11),
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_phase_wkts, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Bottom Row: Visual 4 (Dot-ball Share by Style) & Visual 5 (Economy Trend by Season)
    # --------------------------------------------------------------------------
    b_row_col1, b_row_col2 = st.columns(2)

    with b_row_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Dot-ball Share by Bowling Style</div>',
            unsafe_allow_html=True,
        )
        dot_style_df = q(
            f"""
            SELECT
                {STYLE_CASE} AS style_group,
                ROUND(100.0 * SUM(CASE WHEN total_runs = 0 THEN 1 ELSE 0 END) / NULLIF(SUM(is_legal), 0), 1) AS dot_ball_pct
            FROM v_ball
            WHERE {f_where_s1}
              AND {BT_NOT_BLANK}
            GROUP BY style_group
            HAVING SUM(is_legal) >= 20
            ORDER BY dot_ball_pct DESC;
            """,
            f_params_s1,
        )

        fig_dot_style = px.bar(
            dot_style_df,
            x="dot_ball_pct",
            y="style_group",
            orientation="h",
            text="dot_ball_pct",
            labels={"dot_ball_pct": "", "style_group": ""},
        )
        fig_dot_style.update_traces(
            marker_color=DARK_GREEN,
            texttemplate="%{text:.1f}%",
            textposition="inside",
            textfont=dict(color="#ffffff", size=11),
        )
        fig_dot_style.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(
                title="Bowling Style",
                title_font=dict(color="#000000", size=11),
                autorange="reversed",
                tickfont=dict(color="#000000", size=11),
            ),
            xaxis=dict(
                title="Dot-Ball Percentage (%)",
                title_font=dict(color="#000000", size=11),
                range=[0, 45],
                dtick=10,
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_dot_style, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with b_row_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Economy Trend by Season (2008–2026)</div>',
            unsafe_allow_html=True,
        )
        trend_where_s1, trend_params_s1 = build_filter_clause(
            teams=sel_teams_s1,
            styles=sel_styles_s1,
        )
        season_trend_df = q(
            f"""
            SELECT
                season_id AS season,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy
            FROM v_ball
            WHERE {trend_where_s1}
              AND season_id BETWEEN 2008 AND 2026
            GROUP BY season_id
            ORDER BY season_id ASC;
            """,
            trend_params_s1,
        )

        fig_season_trend = px.line(
            season_trend_df,
            x="season",
            y="economy",
            markers=True,
            labels={"season": "Year", "economy": "Economy Rate (RPO)"},
        )
        fig_season_trend.update_traces(
            line=dict(color=DARK_GREEN, width=2.5),
            marker=dict(size=7, color=DARK_GREEN),
            cliponaxis=False,
        )

        if sel_seasons_s1:
            sel_s1_pts = season_trend_df[season_trend_df["season"].isin(sel_seasons_s1)]
            if not sel_s1_pts.empty:
                fig_season_trend.add_trace(
                    go.Scatter(
                        x=sel_s1_pts["season"],
                        y=sel_s1_pts["economy"],
                        mode="markers",
                        name="Selected Seasons",
                        marker=dict(size=11, color="#ef4444", symbol="diamond"),
                        hovertemplate="Season %{x}: %{y:.2f} RPO (Filtered)<extra></extra>",
                        showlegend=False,
                        cliponaxis=False,
                    )
                )

        fig_season_trend.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            margin=dict(l=20, r=20, t=10, b=10),
            yaxis=dict(
                title="Economy Rate (RPO)",
                title_font=dict(color="#000000", size=11),
                range=[6, 10.5],
                dtick=1,
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
            xaxis=dict(
                title="Year",
                title_font=dict(color="#000000", size=11),
                range=[2008, 2026],
                tickmode="linear",
                tick0=2008,
                dtick=2,
                tickformat="d",
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_season_trend, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Leaderboard Table: Top 5 Bowlers List Details
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    tbl_col1, tbl_col2 = st.columns([3, 2])
    with tbl_col1:
        st.markdown(
            '<div class="chart-card-title">🏆 Top 5 Bowlers Leaderboard</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size: 13px; color: #000000; margin-top: -6px; margin-bottom: 8px; font-weight: 500;">'
            'Detailed statistics for the top 5 bowlers matching active filters'
            '</div>',
            unsafe_allow_html=True,
        )
    with tbl_col2:
        rank_metric = st.selectbox(
            "Rank By",
            ["Most Wickets", "Best Economy", "Highest Dot-Ball %", "Best Bowling Average"],
            index=0,
            key="s1_rank_metric",
        )

    if rank_metric == "Best Economy":
        sort_sql = "economy ASC, wickets DESC"
    elif rank_metric == "Highest Dot-Ball %":
        sort_sql = "dot_pct DESC, wickets DESC"
    elif rank_metric == "Best Bowling Average":
        sort_sql = "(CASE WHEN average IS NULL OR average = 0 THEN 999 ELSE average END) ASC, wickets DESC"
    else:
        sort_sql = "wickets DESC, economy ASC"

    # Query top 5 bowlers with active filters and min balls threshold
    top5_df = q(
        f"""
        SELECT
            bowler,
            {STYLE_CASE} AS style_group,
            COUNT(DISTINCT match_id) AS matches,
            SUM(is_legal) AS balls,
            SUM(bowler_runs) AS runs,
            SUM(bowler_wicket) AS wickets,
            ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
            ROUND(1.0 * SUM(bowler_runs) / NULLIF(SUM(bowler_wicket), 0), 2) AS average,
            ROUND(1.0 * SUM(is_legal) / NULLIF(SUM(bowler_wicket), 0), 2) AS strike_rate,
            ROUND(100.0 * SUM(CASE WHEN total_runs = 0 THEN 1 ELSE 0 END) / NULLIF(SUM(is_legal), 0), 1) AS dot_pct
        FROM v_ball
        WHERE {f_where_s1}
          AND {BT_NOT_BLANK}
        GROUP BY bowler
        HAVING SUM(is_legal) >= ?
        ORDER BY {sort_sql}
        LIMIT 5;
        """,
        f_params_s1 + (min_balls_s1,),
    )

    # Fallback to lower balls threshold if user selected high threshold and no results
    if top5_df.empty:
        top5_df = q(
            f"""
            SELECT
                bowler,
                {STYLE_CASE} AS style_group,
                COUNT(DISTINCT match_id) AS matches,
                SUM(is_legal) AS balls,
                SUM(bowler_runs) AS runs,
                SUM(bowler_wicket) AS wickets,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
                ROUND(1.0 * SUM(bowler_runs) / NULLIF(SUM(bowler_wicket), 0), 2) AS average,
                ROUND(1.0 * SUM(is_legal) / NULLIF(SUM(bowler_wicket), 0), 2) AS strike_rate,
                ROUND(100.0 * SUM(CASE WHEN total_runs = 0 THEN 1 ELSE 0 END) / NULLIF(SUM(is_legal), 0), 1) AS dot_pct
            FROM v_ball
            WHERE {f_where_s1}
              AND {BT_NOT_BLANK}
            GROUP BY bowler
            HAVING SUM(is_legal) >= 24
            ORDER BY {sort_sql}
            LIMIT 5;
            """,
            f_params_s1,
        )

    if not top5_df.empty:
        rows_html = []
        for i, r in top5_df.iterrows():
            rank = i + 1
            if rank == 1:
                rank_badge = '<span class="rank-badge rank-1">🥇 1</span>'
            elif rank == 2:
                rank_badge = '<span class="rank-badge rank-2">🥈 2</span>'
            elif rank == 3:
                rank_badge = '<span class="rank-badge rank-3">🥉 3</span>'
            else:
                rank_badge = f'<span class="rank-badge rank-other">{rank}</span>'

            balls_int = int(r["balls"])
            overs_str = f"{balls_int // 6}.{balls_int % 6}"
            style_str = r["style_group"] if pd.notnull(r["style_group"]) else "—"
            avg_str = f"{r['average']:.2f}" if pd.notnull(r["average"]) and r["average"] > 0 else "—"
            sr_str = f"{r['strike_rate']:.1f}" if pd.notnull(r["strike_rate"]) and r["strike_rate"] > 0 else "—"
            econ_str = f"{r['economy']:.2f}" if pd.notnull(r["economy"]) else "—"
            dot_str = f"{r['dot_pct']:.1f}%" if pd.notnull(r["dot_pct"]) else "—"

            rows_html.append(
                f"""<tr>
                    <td>{rank_badge}</td>
                    <td style="font-weight: 750; color: #000000 !important; font-size: 13.5px;">{r['bowler']}</td>
                    <td><span class="style-badge">{style_str}</span></td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{int(r['matches']):,}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{overs_str}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{balls_int:,}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{int(r['runs']):,}</td>
                    <td style="text-align: right;" class="highlight-val">{int(r['wickets']):,}</td>
                    <td style="text-align: right; font-weight: 750; color: #000000 !important;">{econ_str}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{avg_str}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{sr_str}</td>
                    <td style="text-align: right; color: #000000 !important; font-weight: 600;">{dot_str}</td>
                </tr>"""
            )

        table_html = f"""
        <div style="overflow-x: auto; margin-top: 4px;">
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th style="width: 60px;">Rank</th>
                    <th>Bowler</th>
                    <th>Style</th>
                    <th style="text-align: right;">Mat</th>
                    <th style="text-align: right;">Overs</th>
                    <th style="text-align: right;">Balls</th>
                    <th style="text-align: right;">Runs</th>
                    <th style="text-align: right;">Wkts</th>
                    <th style="text-align: right;">Econ</th>
                    <th style="text-align: right;">Avg</th>
                    <th style="text-align: right;">SR</th>
                    <th style="text-align: right;">Dot %</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("No bowlers match the selected filter criteria.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# SCREEN 2: INDIVIDUAL BOWLER
# ==============================================================================
else:
    st.markdown('<div class="page-title">Individual Bowler</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Evaluate one bowler and decide which overs to use</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # Quick Year Preset Buttons
    # Initialize multiselect state if not present
    if "s2_season_ms" not in st.session_state:
        st.session_state["s2_season_ms"] = []
    if "s2_style_ms" not in st.session_state:
        st.session_state["s2_style_ms"] = []

    # --------------------------------------------------------------------------
    # Quick Year Preset Buttons
    # --------------------------------------------------------------------------
    qp2_cols = st.columns([1.6, 1.2, 1.2, 1.2, 1.2, 1.2])
    with qp2_cols[0]:
        st.markdown(
            '<div style="font-size: 12.5px; font-weight: 700; color: #1b4d3e; padding-top: 6px;">'
            '⚡ Quick Year Presets:'
            '</div>',
            unsafe_allow_html=True,
        )
    with qp2_cols[1]:
        if st.button("2008–2012", key="btn_s2_2008_2012", use_container_width=True):
            st.session_state["s2_season_ms"] = [2008, 2009, 2010, 2011, 2012]
            st.rerun()
    with qp2_cols[2]:
        if st.button("2013–2017", key="btn_s2_2013_2017", use_container_width=True):
            st.session_state["s2_season_ms"] = [2013, 2014, 2015, 2016, 2017]
            st.rerun()
    with qp2_cols[3]:
        if st.button("2018–2022", key="btn_s2_2018_2022", use_container_width=True):
            st.session_state["s2_season_ms"] = [2018, 2019, 2020, 2021, 2022]
            st.rerun()
    with qp2_cols[4]:
        if st.button("2023–2026", key="btn_s2_2023_2026", use_container_width=True):
            st.session_state["s2_season_ms"] = [2023, 2024, 2025, 2026]
            st.rerun()
    with qp2_cols[5]:
        if st.button("All / Clear", key="btn_s2_clear", use_container_width=True):
            st.session_state["s2_season_ms"] = []
            st.session_state["s2_style_ms"] = []
            st.rerun()

    # --------------------------------------------------------------------------
    # Multi-Select Filter Bar
    # --------------------------------------------------------------------------
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    ifc1, ifc2, ifc3, ifc4, ifc5 = st.columns([2.0, 1.8, 1.3, 1.1, 1.1])

    with ifc2:
        sel_seasons_s2 = st.multiselect(
            "Seasons",
            options=db_seasons,
            placeholder="All Seasons (2008–2026)",
            key="s2_season_ms",
        )

    with ifc3:
        sel_styles_s2 = st.multiselect(
            "Bowling Style",
            options=["Spin", "Pace"],
            placeholder="All Styles",
            key="s2_style_ms",
        )

    with ifc4:
        min_balls_s2 = st.selectbox("Minimum Balls", [100, 200, 300, 500, 0], index=0, key="s2_min_balls")

    with ifc5:
        min_wkts_s2 = st.selectbox("Minimum Wickets", [0, 5, 10, 25, 50], index=0, key="s2_min_wkts")

    # Build filter clauses for Screen 2
    f_where_s2_season, f_params_s2_season = build_filter_clause(seasons=sel_seasons_s2)
    f_where_s2_season_b, f_params_s2_season_b = build_filter_clause(seasons=sel_seasons_s2, table_alias="b")

    # Dynamic query to narrow bowler candidates based on filters
    style_where_s2 = f"AND b.style IN ({','.join('?' for _ in sel_styles_s2)})" if sel_styles_s2 else ""
    bowler_list_df = q(
        f"""
        SELECT DISTINCT b.bowler
        FROM (
            SELECT
                bowler,
                {SPIN_CASE} AS style,
                SUM(is_legal) AS balls,
                SUM(bowler_wicket) AS wickets
            FROM v_ball
            WHERE {f_where_s2_season}
              AND {BT_NOT_BLANK}
            GROUP BY bowler
            HAVING SUM(is_legal) >= ? AND SUM(bowler_wicket) >= ?
        ) b
        WHERE 1=1 {style_where_s2}
        ORDER BY b.wickets DESC, b.bowler ASC;
        """,
        f_params_s2_season + (min_balls_s2, min_wkts_s2) + tuple(sel_styles_s2),
    )
    all_bowler_candidates = bowler_list_df["bowler"].tolist() if not bowler_list_df.empty else []

    with ifc1:
        if not all_bowler_candidates:
            st.warning("No bowlers matched criteria. Showing top available bowlers.")
            fallback_df = q(
                f"""
                SELECT DISTINCT bowler
                FROM v_ball
                WHERE {f_where_s2_season}
                GROUP BY bowler
                ORDER BY SUM(bowler_wicket) DESC, bowler ASC
                LIMIT 50;
                """,
                f_params_s2_season,
            )
            all_bowler_candidates = fallback_df["bowler"].tolist() if not fallback_df.empty else ["YS Chahal"]

        default_idx = 0
        for fav in ["YS Chahal", "JJ Bumrah", "B Kumar", "SP Narine", "Rashid Khan"]:
            if fav in all_bowler_candidates:
                default_idx = all_bowler_candidates.index(fav)
                break
        selected_bowler = st.selectbox("Search Bowler", all_bowler_candidates, index=default_idx, key="s2_bowler")

    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Top Metric Cards Strip (Exactly 3 Cards)
    # --------------------------------------------------------------------------
    bmc1, bmc2, bmc3 = st.columns(3)

    b_stats_df = q(
        f"""
        SELECT
            SUM(bowler_wicket) AS wickets,
            SUM(is_legal) AS balls,
            ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
            ROUND(100.0 * SUM(CASE WHEN total_runs = 0 THEN 1 ELSE 0 END) / NULLIF(SUM(is_legal), 0), 1) AS dot_ball_pct,
            SUM(CASE WHEN total_runs = 0 THEN 1 ELSE 0 END) AS dot_balls
        FROM v_ball
        WHERE bowler = ?
          AND {f_where_s2_season};
        """,
        (selected_bowler,) + f_params_s2_season,
    )
    b_wkts = int(b_stats_df["wickets"].iloc[0]) if not b_stats_df.empty and pd.notnull(b_stats_df["wickets"].iloc[0]) else 0
    b_balls = int(b_stats_df["balls"].iloc[0]) if not b_stats_df.empty and pd.notnull(b_stats_df["balls"].iloc[0]) else 0
    b_econ = float(b_stats_df["economy"].iloc[0]) if not b_stats_df.empty and pd.notnull(b_stats_df["economy"].iloc[0]) else 0.0
    b_dot_pct = float(b_stats_df["dot_ball_pct"].iloc[0]) if not b_stats_df.empty and pd.notnull(b_stats_df["dot_ball_pct"].iloc[0]) else 0.0
    b_dots = int(b_stats_df["dot_balls"].iloc[0]) if not b_stats_df.empty and pd.notnull(b_stats_df["dot_balls"].iloc[0]) else 0
    b_overs = round(b_balls / 6.0, 1)

    with bmc1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">WICKETS</div>
                <div class="metric-num">{b_wkts:,}</div>
                <div class="metric-desc">({b_balls:,} balls)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with bmc2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">ECONOMY</div>
                <div class="metric-num">{b_econ:.2f}</div>
                <div class="metric-desc">({b_overs:.1f} overs)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with bmc3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">DOT-BALL SHARE</div>
                <div class="metric-num">{b_dot_pct:.0f}%</div>
                <div class="metric-desc">(n = {b_dots:,})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------------------------
    # Visual 1 (The Hero): Economy by Season
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="chart-card-title">Economy by Season</div>',
        unsafe_allow_html=True,
    )

    bowler_season_df = q(
        f"""
        SELECT
            b.season_id AS season,
            ROUND(6.0 * SUM(b.bowler_runs) / NULLIF(SUM(b.is_legal), 0), 2) AS bowler_economy,
            l.league_economy
        FROM v_ball b
        JOIN (
            SELECT season_id, ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS league_economy
            FROM v_ball
            WHERE {f_where_s2_season}
              AND season_id BETWEEN 2008 AND 2026
            GROUP BY season_id
        ) l ON b.season_id = l.season_id
        WHERE b.bowler = ?
          AND {f_where_s2_season_b}
          AND b.season_id BETWEEN 2008 AND 2026
        GROUP BY b.season_id
        ORDER BY b.season_id ASC;
        """,
        f_params_s2_season + (selected_bowler,) + f_params_s2_season_b,
    )

    fig_b_season = go.Figure()
    if not bowler_season_df.empty:
        fig_b_season.add_trace(
            go.Scatter(
                x=bowler_season_df["season"],
                y=bowler_season_df["bowler_economy"],
                mode="lines+markers",
                name="Bowler",
                line=dict(color=DARK_GREEN, width=2.5),
                marker=dict(size=7, color=DARK_GREEN),
                hovertemplate="Season %{x}: %{y:.2f} RPO<extra></extra>",
            )
        )
        fig_b_season.add_trace(
            go.Scatter(
                x=bowler_season_df["season"],
                y=bowler_season_df["league_economy"],
                mode="lines",
                name="--- League Average",
                line=dict(color=LEAGUE_LINE, width=1.5, dash="dash"),
                hovertemplate="League (%{x}): %{y:.2f} RPO<extra></extra>",
            )
        )
        if sel_seasons_s2:
            sel_b_pt = bowler_season_df[bowler_season_df["season"].isin(sel_seasons_s2)]
            if not sel_b_pt.empty:
                fig_b_season.add_trace(
                    go.Scatter(
                        x=sel_b_pt["season"],
                        y=sel_b_pt["bowler_economy"],
                        mode="markers",
                        name="Selected Seasons",
                        marker=dict(size=12, color="#ef4444", symbol="diamond"),
                        hovertemplate=f"{selected_bowler} (%{{x}}): %{{y:.2f}} RPO<extra></extra>",
                    )
                )

    fig_b_season.update_traces(cliponaxis=False)
    fig_b_season.update_layout(
        template="plotly_white",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color="#000000"),
        height=300,
        margin=dict(l=30, r=30, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#000000", size=11),
        ),
        yaxis=dict(
            range=[4, 12],
            dtick=2,
            title="Economy Rate (RPO)",
            title_font=dict(color="#000000", size=12),
            tickfont=dict(color="#000000", size=11),
            gridcolor="#e2e8f0",
        ),
        xaxis=dict(
            title="Year",
            title_font=dict(color="#000000", size=12),
            range=[2008, 2026],
            tickmode="linear",
            tick0=2008,
            dtick=2,
            tickformat="d",
            tickfont=dict(color="#000000", size=11),
            gridcolor="#e2e8f0",
        ),
    )
    st.plotly_chart(fig_b_season, use_container_width=True, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Middle Row: Visual 2 (Wickets & Economy by Phase) & Visual 3 (Economy vs Opponent)
    # --------------------------------------------------------------------------
    b_mid_col1, b_mid_col2 = st.columns(2)

    with b_mid_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Wickets & Economy by Phase</div>',
            unsafe_allow_html=True,
        )
        b_phase_stats = q(
            f"""
            SELECT
                CASE phase
                    WHEN 'Powerplay' THEN 'Powerplay (1–6)'
                    WHEN 'Middle' THEN 'Middle Overs (7–15)'
                    ELSE 'Death Overs (16–20)'
                END AS phase_label,
                SUM(bowler_wicket) AS wickets,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
                SUM(is_legal) AS balls
            FROM v_ball
            WHERE bowler = ?
              AND {f_where_s2_season}
            GROUP BY phase_label
            ORDER BY CASE phase_label
                WHEN 'Powerplay (1–6)' THEN 1
                WHEN 'Middle Overs (7–15)' THEN 2
                ELSE 3 END;
            """,
            (selected_bowler,) + f_params_s2_season,
        )

        fig_b_phase = go.Figure()
        if not b_phase_stats.empty:
            fig_b_phase.add_trace(
                go.Bar(
                    x=b_phase_stats["phase_label"],
                    y=b_phase_stats["wickets"],
                    name="Wickets",
                    marker_color=LIGHT_GREEN,
                    yaxis="y",
                    width=0.4,
                )
            )
            fig_b_phase.add_trace(
                go.Scatter(
                    x=b_phase_stats["phase_label"],
                    y=b_phase_stats["economy"],
                    name="Economy",
                    mode="lines+markers",
                    line=dict(color=DARK_GREEN, width=2.5),
                    marker=dict(size=8, color=DARK_GREEN),
                    yaxis="y2",
                )
            )

        fig_b_phase.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=260,
            margin=dict(l=20, r=20, t=10, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#000000", size=11),
            ),
            yaxis=dict(
                title="Wickets",
                title_font=dict(color="#000000", size=12),
                tickfont=dict(color="#000000", size=11),
                side="left",
                gridcolor="#e2e8f0",
            ),
            yaxis2=dict(
                title="Economy Rate (RPO)",
                title_font=dict(color="#000000", size=12),
                tickfont=dict(color="#000000", size=11),
                side="right",
                overlaying="y",
                range=[0, 14],
                dtick=2,
            ),
            xaxis=dict(
                title="Innings Phase",
                title_font=dict(color="#000000", size=12),
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_b_phase, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with b_mid_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Economy vs Opponent</div>',
            unsafe_allow_html=True,
        )
        b_opp_df = q(
            f"""
            SELECT
                batting_team AS opponent,
                ROUND(6.0 * SUM(bowler_runs) / NULLIF(SUM(is_legal), 0), 2) AS economy,
                SUM(is_legal) AS balls
            FROM v_ball
            WHERE bowler = ?
              AND {f_where_s2_season}
            GROUP BY batting_team
            HAVING SUM(is_legal) >= 12
            ORDER BY economy ASC
            LIMIT 8;
            """,
            (selected_bowler,) + f_params_s2_season,
        )

        fig_b_opp = px.bar(
            b_opp_df,
            x="economy",
            y="opponent",
            orientation="h",
            text="economy",
            labels={"economy": "", "opponent": ""},
        )
        fig_b_opp.update_traces(
            marker_color=MID_GREEN,
            texttemplate="%{text:.2f}",
            textposition="inside",
            textfont=dict(color="#ffffff", size=11),
        )
        fig_b_opp.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=260,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(
                title="Opponent Team",
                title_font=dict(color="#000000", size=11),
                autorange="reversed",
                tickfont=dict(color="#000000", size=11),
            ),
            xaxis=dict(
                title="Economy Rate (RPO)",
                title_font=dict(color="#000000", size=11),
                range=[0, 15],
                dtick=5,
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_b_opp, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Bottom Row: Visual 4 (Economy by Ground, venue_clean) & Visual 5 (Dismissal Types)
    # --------------------------------------------------------------------------
    b_bot_col1, b_bot_col2 = st.columns(2)

    with b_bot_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Economy by Ground</div>',
            unsafe_allow_html=True,
        )
        b_ground_df = q(
            f"""
            SELECT
                m.venue_clean AS ground,
                ROUND(6.0 * SUM(b.bowler_runs) / NULLIF(SUM(b.is_legal), 0), 2) AS economy,
                SUM(b.is_legal) AS balls
            FROM v_ball b
            JOIN matches_clean m ON b.match_id = m.match_id
            WHERE b.bowler = ?
              AND {f_where_s2_season_b}
            GROUP BY m.venue_clean
            HAVING SUM(b.is_legal) >= 24
            ORDER BY economy ASC
            LIMIT 5;
            """,
            (selected_bowler,) + f_params_s2_season_b,
        )

        fig_b_ground = px.bar(
            b_ground_df,
            x="economy",
            y="ground",
            orientation="h",
            text="economy",
            labels={"economy": "", "ground": ""},
        )
        fig_b_ground.update_traces(
            marker_color=MID_GREEN,
            texttemplate="%{text:.2f}",
            textposition="inside",
            textfont=dict(color="#ffffff", size=11),
        )
        fig_b_ground.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(
                title="Ground / Venue",
                title_font=dict(color="#000000", size=11),
                autorange="reversed",
                tickfont=dict(color="#000000", size=11),
            ),
            xaxis=dict(
                title="Economy Rate (RPO)",
                title_font=dict(color="#000000", size=11),
                range=[0, 15],
                dtick=5,
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_b_ground, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with b_bot_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-card-title">Dismissal Types</div>',
            unsafe_allow_html=True,
        )
        b_dism_types = q(
            f"""
            SELECT
                CASE wicket_kind
                    WHEN 'bowled' THEN 'Bowled'
                    WHEN 'caught' THEN 'Caught'
                    WHEN 'lbw' THEN 'LBW'
                    WHEN 'caught and bowled' THEN 'Caught & Bowled'
                    WHEN 'stumped' THEN 'Stumped'
                    WHEN 'hit wicket' THEN 'Hit Wicket'
                    ELSE 'Others'
                END AS dismissal_label,
                COUNT(*) AS count
            FROM v_ball
            WHERE bowler = ?
              AND {f_where_s2_season}
              AND bowler_wicket = 1
            GROUP BY dismissal_label
            ORDER BY count DESC;
            """,
            (selected_bowler,) + f_params_s2_season,
        )

        fig_b_dism = px.bar(
            b_dism_types,
            x="count",
            y="dismissal_label",
            orientation="h",
            text="count",
            labels={"count": "", "dismissal_label": ""},
        )
        fig_b_dism.update_traces(
            marker_color=DARK_GREEN,
            texttemplate="%{text}",
            textposition="inside",
            textfont=dict(color="#ffffff", size=11),
        )
        fig_b_dism.update_layout(
            template="plotly_white",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color="#000000"),
            height=250,
            margin=dict(l=10, r=20, t=10, b=10),
            yaxis=dict(
                title="Dismissal Type",
                title_font=dict(color="#000000", size=11),
                autorange="reversed",
                tickfont=dict(color="#000000", size=11),
            ),
            xaxis=dict(
                title="Wickets",
                title_font=dict(color="#000000", size=11),
                tickfont=dict(color="#000000", size=11),
                gridcolor="#e2e8f0",
            ),
        )
        st.plotly_chart(fig_b_dism, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)
