import streamlit as st
import pandas as pd
import sys
import numpy as np
import plotly.graph_objects as go
from utils.data import (
    get_connection,
    load_undervalued,
    load_photos,
    search_players,
    get_all_player_names,
    load_compare_players,
)

sys.path.append('.')

st.set_page_config(
    page_title="Football Moneyball — Valuation System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- GROUNDED SPORTS ANALYTICS DESIGN SYSTEM ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9;
    }

    /* Page Container */
    .main .block-container {
        max-width: 1240px;
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
    }

    /* Top Navigation Tabs */
    div[data-testid="stColumn"] > div > div > div > button {
        border-radius: 6px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border: 1px solid #273244 !important;
        background-color: #141a24 !important;
        color: #94a3b8 !important;
        padding: 0.5rem 0.85rem !important;
        transition: border-color 0.15s ease, color 0.15s ease, background-color 0.15s ease !important;
        box-shadow: none !important;
    }
    div[data-testid="stColumn"] > div > div > div > button:hover {
        border-color: #38bdf8 !important;
        color: #f1f5f9 !important;
        background-color: #1c2432 !important;
    }

    /* Grounded Scout Card Container */
    .scout-card {
        background-color: #141a24;
        border: 1px solid #273244;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .scout-card-header {
        font-family: 'Barlow', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.2px;
    }

    /* Typography & Hierarchy */
    .system-title {
        font-family: 'Barlow', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #f1f5f9;
        letter-spacing: -0.5px;
        line-height: 1.15;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
    }
    .system-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    .stat-hero-number {
        font-family: 'Barlow', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #10b981;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .stat-hero-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.35rem;
    }

    /* Grounded Badges */
    .badge-uv {
        background-color: #064e3b;
        color: #34d399;
        border: 1px solid #047857;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .badge-ov {
        background-color: #7f1d1d;
        color: #f87171;
        border: 1px solid #b91c1c;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .badge-pos {
        background-color: #1e293b;
        color: #cbd5e1;
        border: 1px solid #334155;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }

    /* Avatar Placeholder Box */
    .avatar-placeholder {
        width: 60px;
        height: 60px;
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Barlow', sans-serif;
        font-weight: 700;
        color: #64748b;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- DIALOG MODALS FOR TERMS & PRIVACY ----------
if hasattr(st, 'dialog'):
    @st.dialog("Terms of Service")
    def show_terms_dialog():
        st.markdown("""
        ### Football Moneyball System — Terms of Service
        **Effective Date:** January 1, 2026

        1. **Acceptance of Terms**
           By accessing and using this application, you agree to be bound by these Terms of Service.

        2. **Analytical Data Disclaimer**
           All market valuations, predicted values, and player rankings are produced by an automated statistical model for analytical research and educational purposes only. They do not constitute financial advice, official scouting valuations, or binding contract offers.

        3. **Data Sources & Intellectual Property**
           Player information, match statistics, and market valuations are sourced from public Transfermarkt datasets and StatsBomb Open Data repositories. Original raw data rights remain with their respective rights holders.

        4. **Limitation of Liability**
           The system authors are not liable for any scouting decisions, financial transfers, or operational actions undertaken based on model outputs.
        """)

    @st.dialog("Privacy Policy")
    def show_privacy_dialog():
        st.markdown("""
        ### Football Moneyball System — Privacy Policy
        **Effective Date:** January 1, 2026

        1. **Data Collection**
           This application operates purely as an analytical reporting interface. We do not collect, harvest, sell, or store personal user identifiers, login credentials, or tracking cookies.

        2. **Session Storage**
           Temporary session states (such as selected player names or filter options) are retained solely in local browser memory for the active session duration and are discarded upon browser closure.

        3. **Third-Party Services**
           The app is hosted on Streamlit Cloud. Images are loaded directly from official source media servers without intermediate user tracking.

        4. **Contact & Queries**
           For data inquiries or methodology questions, reference the open-source repository at [GitHub](https://github.com/yangatsinghsandhu-tech/football-transfer-analysis).
        """)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'show_terms' not in st.session_state:
    st.session_state.show_terms = False
if 'show_privacy' not in st.session_state:
    st.session_state.show_privacy = False

def go_to(page_name):
    st.session_state.page = page_name

# ---------- TOP NAV TAB BAR ----------
n1, n2, n3, n4, n5 = st.columns([1.8, 1, 1, 1, 1])
with n1:
    if st.button("Moneyball Overview", use_container_width=True):
        go_to('home')
with n2:
    if st.button("Undervalued Index", use_container_width=True):
        go_to('undervalued')
with n3:
    if st.button("Player Comparison", use_container_width=True):
        go_to('compare')
with n4:
    if st.button("Player Search", use_container_width=True):
        go_to('search')
with n5:
    if st.button("Model Insights", use_container_width=True):
        go_to('insights')

st.divider()

# ---------- HOME PAGE (ASYMMETRICAL TACTICAL DASHBOARD) ----------
if st.session_state.page == 'home':
    st.markdown('<div class="system-title">Football Moneyball Valuation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="system-subtitle">Quantitative Player Valuation & Undervalued Asset Discovery Engine</div>', unsafe_allow_html=True)

    # Asymmetrical 2-Column Core Layout (Left 2/3, Right 1/3)
    main_col, side_col = st.columns([2.2, 1.1])

    with main_col:
        # System Metric Summary Grid
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("""
            <div class="scout-card" style="text-align: center; padding: 1rem;">
                <div class="stat-hero-number">40,684</div>
                <div class="stat-hero-label">Player Seasons Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("""
            <div class="scout-card" style="text-align: center; padding: 1rem;">
                <div class="stat-hero-number">2018–2026</div>
                <div class="stat-hero-label">Historical Coverage</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown("""
            <div class="scout-card" style="text-align: center; padding: 1rem;">
                <div class="stat-hero-number">0.57</div>
                <div class="stat-hero-label">Model R² Precision</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="scout-card">
            <div class="scout-card-header">Quantitative Scouting Framework</div>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-top: 0.5rem;">
                The valuation engine evaluates per-90 performance metrics (goals, assists, minutes, yellow cards), 
                positional profiles, player age curves, and league tier coefficients against actual transfer market prices. 
                Players priced significantly below model expectations represent target acquisition opportunities.
            </p>
            <div style="background-color: #0b0f17; border: 1px solid #273244; padding: 0.75rem 1rem; border-radius: 6px; font-family: monospace; color: #38bdf8; font-size: 0.85rem; margin-top: 0.75rem;">
                Valuation Ratio = Model Predicted Market Value (€) / Actual Market Value (€)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.5rem;'>Tactical Modules</div>", unsafe_allow_html=True)
        act1, act2, act3 = st.columns(3)
        with act1:
            if st.button("Browse Undervalued Index", use_container_width=True):
                go_to('undervalued')
        with act2:
            if st.button("Compare Player Profiles", use_container_width=True):
                go_to('compare')
        with act3:
            if st.button("Lookup Player Stats", use_container_width=True):
                go_to('search')

    with side_col:
        st.markdown("""
        <div class="scout-card" style="border-color: #10b981;">
            <div style="font-family: 'Barlow', sans-serif; font-size: 0.85rem; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 0.8px;">Scouting Spotlight</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-top: 0.2rem; margin-bottom: 0.75rem;">Top Undervalued Assets (2025)</div>
        </div>
        """, unsafe_allow_html=True)

        # Real-time top 3 undervalued players query
        with st.spinner("Fetching spotlight data..."):
            spotlight_df = load_undervalued(season=2025).head(3)
            photos = load_photos(spotlight_df['name'].tolist())
            spotlight_df = spotlight_df.merge(photos, on='name', how='left')

        for _, row in spotlight_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="scout-card" style="padding: 0.85rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-weight: 700; font-size: 0.95rem; color: #f1f5f9;">{row['name']}</div>
                            <div style="font-size: 0.78rem; color: #94a3b8;">{row['position']} · Age {row['age_at_season']}</div>
                        </div>
                        <div class="badge-uv">{row['value_ratio']:.1f}x</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.6rem; font-size: 0.8rem; color: #cbd5e1;">
                        <span>Actual: €{row['actual_value_eur']:,.0f}</span>
                        <span style="color: #34d399; font-weight: 600;">Model: €{row['predicted_value_eur']:,.0f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ---------- UNDERVALUED INDEX PAGE ----------
elif st.session_state.page == 'undervalued':
    st.markdown('<div class="system-title">Undervalued Player Index</div>', unsafe_allow_html=True)
    st.markdown('<div class="system-subtitle">Ranked inventory of players priced below statistical model valuation</div>', unsafe_allow_html=True)

    filter_c1, filter_c2, filter_c3 = st.columns([2, 1, 1.5])
    with filter_c1:
        search_query = st.text_input("Filter player by name", placeholder="e.g. Musiala, Rodri...")
    with filter_c2:
        season = st.selectbox("Season", [2025, 2024, 2023], index=0)
    with filter_c3:
        positions = st.multiselect("Position Group", ["Attack", "Midfield", "Defender", "Goalkeeper"], default=["Attack", "Midfield"])

    with st.spinner("Processing valuation calculations..."):
        df = load_undervalued(season=season, positions=positions)
        if search_query:
            df = df[df['name'].str.contains(search_query, case=False, na=False)]

    st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem; margin-bottom: 1rem;'>Showing <strong>{len(df)}</strong> players meeting evaluation criteria</div>", unsafe_allow_html=True)

    if len(df) == 0:
        st.info("No players match the specified filters. Adjust position group or search parameters.")
    else:
        if 'show_count' not in st.session_state:
            st.session_state.show_count = 20

        visible_df = df.head(st.session_state.show_count)
        photos = load_photos(visible_df['name'].tolist())
        visible_df = visible_df.merge(photos, on='name', how='left')

        for i, row in visible_df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([0.8, 3, 2, 2.2])
                with c1:
                    if pd.notna(row['image_url']) and str(row['image_url']).startswith('http'):
                        st.image(row['image_url'], width=55)
                    else:
                        initials = "".join([part[0] for part in str(row['name']).split()[:2]]).upper()
                        st.markdown(f"<div class='avatar-placeholder'>{initials}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div style='font-weight: 700; font-size: 1.05rem; color: #f1f5f9;'>{row['name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='badge-pos'>{row['position']}</span> <span style='font-size: 0.8rem; color: #94a3b8;'>Age {row['age_at_season']}</span>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<div class='badge-uv'>{row['value_ratio']:.2f}x Undervalued</div>", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"<div style='font-size: 0.82rem; color: #94a3b8;'>Actual: <strong style='color: #f1f5f9;'>€{row['actual_value_eur']:,.0f}</strong></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.82rem; color: #94a3b8;'>Model: <strong style='color: #34d399;'>€{row['predicted_value_eur']:,.0f}</strong></div>", unsafe_allow_html=True)

                with st.expander("Performance breakdown"):
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.metric("Goals / 90", f"{row['goals_per_90']:.2f}")
                    sc2.metric("Assists / 90", f"{row['assists_per_90']:.2f}")
                    sc3.metric("Total Minutes", f"{row['total_minutes']:,.0f}")

                st.divider()

        if st.session_state.show_count < len(df):
            if st.button("Load 20 More Players"):
                st.session_state.show_count += 20
                st.rerun()

# ---------- PLAYER COMPARISON PAGE ----------
elif st.session_state.page == 'compare':
    st.markdown('<div class="system-title">Head-to-Head Player Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="system-subtitle">Multi-metric performance overlay and comparative valuation assessment</div>', unsafe_allow_html=True)

    all_names = get_all_player_names()
    selected_players = st.multiselect("Select 2 or more players for comparative evaluation", all_names)

    if len(selected_players) >= 2:
        season_cmp = st.selectbox("Season", [2025, 2024, 2023], index=0, key="cmp_season")
        with st.spinner("Compiling comparative metrics..."):
            cmp_df = load_compare_players(selected_players, season_cmp)

        found_names = cmp_df['name'].tolist()
        missing_names = [n for n in selected_players if n not in found_names]
        if missing_names:
            st.warning(f"Insufficient season data for: {', '.join(missing_names)} in {season_cmp}.")

        if len(cmp_df) < 2:
            st.info("Select at least 2 players with available data in the selected season.")
        else:
            photos = load_photos(cmp_df['name'].tolist())
            cmp_df = cmp_df.merge(photos, on='name', how='left')

            photo_cols = st.columns(len(cmp_df))
            for idx, (i, row) in enumerate(cmp_df.iterrows()):
                with photo_cols[idx]:
                    if pd.notna(row['image_url']) and str(row['image_url']).startswith('http'):
                        st.image(row['image_url'], width=70)
                    st.markdown(f"**{row['name']}**")
                    st.caption(f"{row['position']} · Age {row['age_at_season']}")

            st.divider()

            # Plotly Grouped Bar Chart (Grounded Slate Theme)
            stats = ['goals_per_90', 'assists_per_90']
            labels = ['Goals / 90', 'Assists / 90']

            fig = go.Figure()
            palette = ['#10b981', '#0284c7', '#f59e0b', '#ec4899', '#8b5cf6']
            for i, (idx, row) in enumerate(cmp_df.iterrows()):
                color = palette[i % len(palette)]
                fig.add_trace(go.Bar(
                    x=labels,
                    y=row[stats].values,
                    name=row['name'],
                    marker_color=color,
                    hovertemplate="<b>%{x}</b>: %{y:.2f}<extra>" + row['name'] + "</extra>"
                ))

            fig.update_layout(
                barmode='group',
                paper_bgcolor='#141a24',
                plot_bgcolor='#141a24',
                font=dict(color='#f1f5f9', family='IBM Plex Sans'),
                xaxis=dict(showgrid=False, tickfont=dict(color='#cbd5e1', size=12), zeroline=False),
                yaxis=dict(gridcolor='#273244', tickfont=dict(color='#94a3b8'), zerolinecolor='#273244'),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=20, t=40, b=40),
                height=360
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            display_df = cmp_df[['name', 'position', 'age_at_season', 'total_minutes', 'actual_value_eur', 'predicted_value_eur']].copy()
            display_df.columns = ['Player', 'Position', 'Age', 'Minutes', 'Actual Value', 'Predicted Value']
            display_df['Actual Value'] = display_df['Actual Value'].apply(lambda x: f'€{x:,.0f}')
            display_df['Predicted Value'] = display_df['Predicted Value'].apply(lambda x: f'€{x:,.0f}')
            st.dataframe(display_df, hide_index=True, use_container_width=True)
    else:
        st.info("Select at least 2 players from the search selector above to compare.")

# ---------- PLAYER SEARCH PAGE ----------
elif st.session_state.page == 'search':
    st.markdown('<div class="system-title">Player Directory & Stats Lookup</div>', unsafe_allow_html=True)
    st.markdown('<div class="system-subtitle">Comprehensive profile search across historical player predictions</div>', unsafe_allow_html=True)

    all_names = get_all_player_names()
    selected_name = st.selectbox(
        "Search or select player name",
        options=[""] + all_names,
        index=0,
        placeholder="Type to search player name (e.g. Jamal Musiala, Rodri, Bellingham...)",
        key="search_player_selectbox"
    )

    if not selected_name:
        st.info("Select or type a player name in the search control above to display technical stats and market value.")
    else:
        with st.spinner("Retrieving player records..."):
            search_df = search_players(selected_name)

        if len(search_df) == 0:
            st.info("No player records found matching that selection.")
        else:
            player_matches = search_df[search_df['name'] == selected_name]
            if len(player_matches) == 0:
                player_matches = search_df

            distinct_pids = player_matches[['player_id', 'position', 'current_club_name']].drop_duplicates(subset=['player_id'])
            if len(distinct_pids) > 1:
                pid_labels = {row['player_id']: f"{selected_name} ({row['position']} · {row['current_club_name'] or 'Unknown Club'})" for _, row in distinct_pids.iterrows()}
                selected_pid = st.selectbox("Select Player Profile", list(pid_labels.keys()), format_func=lambda x: pid_labels[x], key="search_player_id_select")
                player_df = player_matches[player_matches['player_id'] == selected_pid]
            else:
                player_df = player_matches

            available_seasons = sorted(player_df['season_year'].unique().tolist(), reverse=True)
            if len(available_seasons) > 1:
                selected_season = st.selectbox("Season", available_seasons, index=0, key="search_season_select")
                season_row = player_df[player_df['season_year'] == selected_season].iloc[0]
            else:
                season_row = player_df.iloc[0]

            st.divider()

            with st.container():
                head_c1, head_c2 = st.columns([1, 4])
                with head_c1:
                    if pd.notna(season_row['image_url']) and str(season_row['image_url']).startswith('http'):
                        st.image(season_row['image_url'], width=110)
                    else:
                        initials = "".join([part[0] for part in str(season_row['name']).split()[:2]]).upper()
                        st.markdown(f"<div class='avatar-placeholder' style='width: 90px; height: 90px; font-size: 1.8rem;'>{initials}</div>", unsafe_allow_html=True)
                
                with head_c2:
                    st.title(season_row['name'])
                    club_info = season_row['current_club_name'] or "Club N/A"
                    comp_info = f" ({season_row['competition_name']})" if pd.notna(season_row['competition_name']) else ""
                    st.markdown(f"**{season_row['position']}** · Age **{season_row['age_at_season']}** · **{club_info}{comp_info}**")
                    st.caption(f"Evaluation Season: {season_row['season_year']}")

                st.divider()

                val_c1, val_c2, val_c3 = st.columns(3)
                with val_c1:
                    st.metric("Actual Market Value", f"€{season_row['actual_value_eur']:,.0f}")
                with val_c2:
                    st.metric("Model Predicted Value", f"€{season_row['predicted_value_eur']:,.0f}")
                with val_c3:
                    ratio = season_row['value_ratio']
                    diff = season_row['predicted_value_eur'] - season_row['actual_value_eur']
                    if ratio > 1.0:
                        st.metric("Valuation Ratio", f"{ratio:.2f}x", delta=f"Undervalued by €{diff:,.0f}", delta_color="normal")
                    else:
                        st.metric("Valuation Ratio", f"{ratio:.2f}x", delta=f"Overvalued by €{-diff:,.0f}", delta_color="inverse")

                st.divider()

                st.subheader(f"Per-90 Technical Stats ({season_row['season_year']} Season)")
                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Goals / 90", f"{season_row['goals_per_90']:.2f}")
                s2.metric("Assists / 90", f"{season_row['assists_per_90']:.2f}")
                s3.metric("Total Minutes", f"{season_row['total_minutes']:,.0f}")
                s4.metric("Yellows / 90", f"{season_row['yellows_per_90']:.2f}")

                st.write("")
                meta_c1, meta_c2 = st.columns(2)
                with meta_c1:
                    caps = int(season_row['international_caps']) if pd.notna(season_row['international_caps']) else 0
                    st.markdown(f"**International Caps:** {caps}")
                with meta_c2:
                    height = f"{season_row['height_in_cm']} cm" if pd.notna(season_row['height_in_cm']) else "N/A"
                    st.markdown(f"**Height:** {height}")

# ---------- MODEL INSIGHTS PAGE ----------
elif st.session_state.page == 'insights':
    st.markdown('<div class="system-title">Model Architecture & Feature Weights</div>', unsafe_allow_html=True)
    st.markdown('<div class="system-subtitle">Log-Linear Regression statistical breakdown, feature coefficients, and scope limitations</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Architecture", "Log-Linear Regression")
    m2.metric("Variance Explained (R²)", "0.57")
    m3.metric("Mean Absolute Error (MAE)", "≈ 0.77 (log scale)")

    st.divider()

    st.subheader("Methodology Overview")
    st.markdown("""
    The valuation model estimates a player's **logarithmic transfer market value** $\\log(\\text{Market Value in EUR})$ 
    by evaluating per-90 performance metrics, age trajectories, positional assignments, and competition tier signals.
    
    - **Target Variable:** $\\log(\\text{Market Value in EUR})$
    - **Feature Inputs:**
      - **Performance (per-90):** `goals_per_90`, `assists_per_90`, `yellows_per_90`, `total_minutes`
      - **Positional One-Hot:** `pos_attack`, `pos_midfield`, `pos_defender`, `pos_goalkeeper`
      - **Demographic Curve:** `age_at_season`, `age_squared` (quadratic age peak), `height_in_cm`, `international_caps`
      - **League Quality Signal:** `is_top5_league` (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)
    """)

    st.divider()

    st.subheader("Feature Coefficients")
    st.markdown("Linear regression coefficients mapped on log market value. Positive values driver higher predicted market valuation, while negative values penalize market valuation.")

    coefficients = {
        'assists_per_90': 1.194646,
        'is_top5_league': 1.152143,
        'goals_per_90': 1.042763,
        'age_at_season': 0.558421,
        'pos_midfield': 0.088248,
        'international_caps': 0.013137,
        'total_minutes': 0.000589,
        'height_in_cm': -0.000861,
        'pos_attack': -0.009331,
        'pos_defender': -0.010669,
        'age_squared': -0.012115,
        'pos_goalkeeper': -0.068248,
        'yellows_per_90': -0.152751,
    }

    sorted_coefs = dict(sorted(coefficients.items(), key=lambda x: x[1]))
    features = list(sorted_coefs.keys())
    vals = list(sorted_coefs.values())

    bar_colors = ['#10b981' if v > 0 else '#f43f5e' for v in vals]

    fig = go.Figure(go.Bar(
        x=vals,
        y=features,
        orientation='h',
        marker_color=bar_colors,
        text=[f"{v:+.4f}" for v in vals],
        textposition='outside',
        textfont=dict(color='#f1f5f9', size=11, family='IBM Plex Sans'),
        hovertemplate="<b>%{y}</b><br>Coefficient: %{x:+.4f}<extra></extra>"
    ))

    fig.update_layout(
        paper_bgcolor='#141a24',
        plot_bgcolor='#141a24',
        font=dict(color='#f1f5f9', family='IBM Plex Sans'),
        xaxis=dict(title=dict(text="Coefficient Weight on Log Market Value", font=dict(color='#94a3b8', size=12)), gridcolor='#273244', tickfont=dict(color='#94a3b8'), zerolinecolor='#94a3b8', zerolinewidth=1.5),
        yaxis=dict(showgrid=False, tickfont=dict(color='#cbd5e1', size=11)),
        margin=dict(l=130, r=60, t=30, b=40),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Technical Scope & Limitations")
    st.markdown("""
    1. **Defensive Action Action Gaps (Tackles, Interceptions, Clearances)**
       - The current dataset relies primarily on box-score offensive outputs.
       - **Impact:** Central defenders, defensive midfielders, and goalkeepers cannot be evaluated fairly on defensive actions.
       - **Future Direction:** Integrating **StatsBomb Open Data** ([github.com/statsbomb/open-data](https://github.com/statsbomb/open-data)) as a primary event data provider.

    2. **Single Global Age Curve**
       - The model applies a single global quadratic age trajectory (`age` + `age²`), setting an estimated valuation peak around **~23 years old**.
       - **Impact:** This peak is unrealistically early for central midfielders and defenders who typically peak between ages 27–30.

    3. **Contractual & Off-Pitch Variables**
       - Market valuations in European football are strongly influenced by factors outside on-pitch box stats.
       - **Impact:** Signals for remaining contract length, injury history, and media narrative are unmodeled in this baseline.
    """)

# ---------- FOOTER & LEGAL MODAL CONTROLS ----------
st.divider()
footer_c1, footer_c2, footer_c3 = st.columns([2, 2, 2])

with footer_c1:
    st.markdown("<div style='font-size: 0.8rem; color: #64748b;'>Football Moneyball System v1.4</div>", unsafe_allow_html=True)
with footer_c2:
    f_btn1, f_btn2 = st.columns(2)
    with f_btn1:
        if st.button("Terms of Service", key="btn_terms_footer"):
            if hasattr(st, 'dialog'):
                show_terms_dialog()
            else:
                st.info("Terms of Service: Analytical model outputs are for research and educational purposes only.")
    with f_btn2:
        if st.button("Privacy Policy", key="btn_privacy_footer"):
            if hasattr(st, 'dialog'):
                show_privacy_dialog()
            else:
                st.info("Privacy Policy: No personal identifiers or tracking cookies are collected or stored.")

with footer_c3:
    st.markdown("<div style='font-size: 0.8rem; color: #64748b; text-align: right;'>Data Sources: Transfermarkt & StatsBomb</div>", unsafe_allow_html=True)