import streamlit as st
import pandas as pd
import sys
import numpy as np
import plotly.graph_objects as go
from utils.data import get_connection, load_undervalued, load_photos, search_players, get_all_player_names
sys.path.append('.')

st.set_page_config(
    page_title="Football Moneyball",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS STYLING ----------
st.markdown("""
<style>
    /* Global Page Fade-In Animation */
    @keyframes pageFadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container {
        animation: pageFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        max-width: 1200px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    /* Top Navigation Button Styling (Pill Tabs) */
    div[data-testid="stColumn"] > div > div > div > button {
        border-radius: 24px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stColumn"] > div > div > div > button:hover {
        border-color: #00e676 !important;
        color: #00e676 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 14px rgba(0, 230, 118, 0.2) !important;
    }

    /* Card Container Styling */
    .fotmob-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease, box-shadow 0.22s ease;
    }
    .fotmob-card:hover {
        transform: translateY(-3px);
        border-color: #00e676;
        box-shadow: 0 8px 24px rgba(0, 230, 118, 0.15);
    }

    /* Metric & Typography Enhancements */
    .headline-stat {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00e676;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .sub-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    
    /* Value Badges */
    .badge-uv {
        background-color: rgba(0, 230, 118, 0.15);
        color: #00e676;
        border: 1px solid rgba(0, 230, 118, 0.35);
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-ov {
        background-color: rgba(255, 82, 82, 0.15);
        color: #ff5252;
        border: 1px solid rgba(255, 82, 82, 0.35);
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to(page_name):
    st.session_state.page = page_name

# ---------- TOP NAV ----------
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([2.2, 1, 1, 1, 1])
with nav_col1:
    if st.button("⚽ Football Moneyball", use_container_width=True):
        go_to('home')
with nav_col2:
    if st.button("📉 Undervalued", use_container_width=True):
        go_to('undervalued')
with nav_col3:
    if st.button("⚖️ Compare", use_container_width=True):
        go_to('compare')
with nav_col4:
    if st.button("🔍 Search", use_container_width=True):
        go_to('search')
with nav_col5:
    if st.button("📊 Insights", use_container_width=True):
        go_to('insights')

st.divider()

# ---------- HOME PAGE ----------
if st.session_state.page == 'home':
    st.title("⚽ Football Transfer Market Value Model")
    st.markdown("""
    Identify **undervalued football players** across European leagues by evaluating performance metrics 
    against a statistical model of transfer market valuations.
    """)

    # Animated JS Count-Up Component
    st.components.v1.html("""
    <div style="display: flex; justify-content: space-around; background: #161b22; border: 1px solid #30363d; border-radius: 16px; padding: 1.5rem; margin-top: 0.8rem; margin-bottom: 1.2rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
        <div style="flex: 1;">
            <div id="cnt-players" style="font-size: 2.6rem; font-weight: 800; color: #00e676; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; letter-spacing: -0.5px;">0</div>
            <div style="font-size: 0.82rem; color: #8b949e; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; margin-top: 0.4rem; font-family: sans-serif;">PLAYERS ANALYZED</div>
        </div>
        <div style="border-left: 1px solid #30363d;"></div>
        <div style="flex: 1;">
            <div style="font-size: 2.6rem; font-weight: 800; color: #00e676; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; letter-spacing: -0.5px;">2018–2026</div>
            <div style="font-size: 0.82rem; color: #8b949e; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; margin-top: 0.4rem; font-family: sans-serif;">SEASONS COVERED</div>
        </div>
        <div style="border-left: 1px solid #30363d;"></div>
        <div style="flex: 1;">
            <div id="cnt-r2" style="font-size: 2.6rem; font-weight: 800; color: #00e676; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; letter-spacing: -0.5px;">0.00</div>
            <div style="font-size: 0.82rem; color: #8b949e; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; margin-top: 0.4rem; font-family: sans-serif;">MODEL ACCURACY (R²)</div>
        </div>
    </div>
    <script>
        function runCount(id, start, end, duration, decimals) {
            let el = document.getElementById(id);
            if (!el) return;
            let startT = null;
            function step(t) {
                if (!startT) startT = t;
                let p = Math.min((t - startT) / duration, 1);
                let val = p * (end - start) + start;
                el.innerHTML = decimals > 0 ? val.toFixed(decimals) : Math.floor(val).toLocaleString();
                if (p < 1) window.requestAnimationFrame(step);
            }
            window.requestAnimationFrame(step);
        }
        runCount('cnt-players', 0, 40684, 1400, 0);
        runCount('cnt-r2', 0.0, 0.57, 1400, 2);
    </script>
    """, height=140)

    st.subheader("Explore Dashboard Features")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        with st.container():
            st.markdown("""
            <div class="fotmob-card" style="min-height: 170px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📉</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #f0f6fc;">Undervalued</div>
                <div style="font-size: 0.85rem; color: #8b949e; margin-top: 0.3rem; margin-bottom: 1rem;">Ranked players priced below model prediction</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Explore Undervalued →", key="home_uv", use_container_width=True):
                go_to('undervalued')

    with b2:
        with st.container():
            st.markdown("""
            <div class="fotmob-card" style="min-height: 170px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚖️</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #f0f6fc;">Compare</div>
                <div style="font-size: 0.85rem; color: #8b949e; margin-top: 0.3rem; margin-bottom: 1rem;">Head-to-head performance comparison</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Compare Players →", key="home_cmp", use_container_width=True):
                go_to('compare')

    with b3:
        with st.container():
            st.markdown("""
            <div class="fotmob-card" style="min-height: 170px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #f0f6fc;">Search</div>
                <div style="font-size: 0.85rem; color: #8b949e; margin-top: 0.3rem; margin-bottom: 1rem;">Full player lookup & stats breakdown</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Search Player →", key="home_search", use_container_width=True):
                go_to('search')

    with b4:
        with st.container():
            st.markdown("""
            <div class="fotmob-card" style="min-height: 170px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #f0f6fc;">Model Insights</div>
                <div style="font-size: 0.85rem; color: #8b949e; margin-top: 0.3rem; margin-bottom: 1rem;">Methodology, coefficients & limitations</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Insights →", key="home_insights", use_container_width=True):
                go_to('insights')

# ---------- UNDERVALUED PAGE ----------
elif st.session_state.page == 'undervalued':
    st.subheader("📉 Undervalued Players")

    search_query = st.text_input("Search player by name", placeholder="e.g. Musiala, Rodri...")

    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Season", [2025, 2024, 2023], index=0)
    with col2:
        positions = st.multiselect("Position", ["Attack", "Midfield", "Defender", "Goalkeeper"],
                                     default=["Attack", "Midfield"])

    df = load_undervalued(season=season, positions=positions)

    if search_query:
        df = df[df['name'].str.contains(search_query, case=False, na=False)]

    st.markdown(f"**{len(df)} players found**")
    st.divider()

    if len(df) == 0:
        st.info("No players found matching that search. Try a different name or adjust the filters.")
    else:
        if 'show_count' not in st.session_state:
            st.session_state.show_count = 20

        visible_df = df.head(st.session_state.show_count)
        photos = load_photos(visible_df['name'].tolist())
        visible_df = visible_df.merge(photos, on='name', how='left')

        for i, row in visible_df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 3, 2, 2])
                with c1:
                    if pd.notna(row['image_url']) and str(row['image_url']).startswith('http'):
                        st.image(row['image_url'], width=65)
                    else:
                        st.markdown("<div style='font-size: 45px; text-align: center;'>👤</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<span style='font-size: 1.15rem; font-weight: 700; color: #f0f6fc;'>{row['name']}</span>", unsafe_allow_html=True)
                    st.caption(f"{row['position']} · Age {row['age_at_season']}")
                with c3:
                    st.markdown(f"<div class='badge-uv'>{row['value_ratio']:.1f}x Undervalued</div>", unsafe_allow_html=True)
                with c4:
                    st.write(f"Actual: **€{row['actual_value_eur']:,.0f}**")
                    st.write(f"Predicted: **€{row['predicted_value_eur']:,.0f}**")

                with st.expander("Full stats"):
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.metric("Goals / 90", f"{row['goals_per_90']:.2f}")
                    sc2.metric("Assists / 90", f"{row['assists_per_90']:.2f}")
                    sc3.metric("Total Minutes", f"{row['total_minutes']:.0f}")

                st.divider()

        if st.session_state.show_count < len(df):
            if st.button("Show more"):
                st.session_state.show_count += 20
                st.rerun()

# ---------- COMPARE PAGE ----------
elif st.session_state.page == 'compare':
    st.subheader("⚖️ Compare Players")

    con = get_connection()
    all_names = con.execute("SELECT DISTINCT name FROM player_predictions ORDER BY name").df()['name'].tolist()

    selected_players = st.multiselect("Select players to compare (2 or more)", all_names)

    if len(selected_players) >= 2:
        season_cmp = st.selectbox("Season", [2025, 2024, 2023], index=0, key="cmp_season")

        placeholders = ", ".join(["?"] * len(selected_players))
        query = f"""
            SELECT name, position, age_at_season, goals_per_90, assists_per_90,
                   total_minutes, actual_value_eur, predicted_value_eur
            FROM player_predictions
            WHERE name IN ({placeholders}) AND season_year = ?
        """
        cmp_df = con.execute(query, selected_players + [season_cmp]).df()
        cmp_df = cmp_df.drop_duplicates(subset='name')

        found_names = cmp_df['name'].tolist()
        missing_names = [n for n in selected_players if n not in found_names]
        if missing_names:
            st.warning(f"No {season_cmp} season data for: {', '.join(missing_names)}. Try a different season for them.")

        if len(cmp_df) < 2:
            st.warning("Not enough data for these players in the selected season. Try a different season.")
        else:
            photos = load_photos(cmp_df['name'].tolist())
            cmp_df = cmp_df.merge(photos, on='name', how='left')

            photo_cols = st.columns(len(cmp_df))
            for idx, (i, row) in enumerate(cmp_df.iterrows()):
                with photo_cols[idx]:
                    if pd.notna(row['image_url']) and str(row['image_url']).startswith('http'):
                        st.image(row['image_url'], width=80)
                    st.markdown(f"**{row['name']}**")
                    st.caption(f"{row['position']} · Age {row['age_at_season']}")

            st.divider()

            # Plotly Multi-Bar Chart
            stats = ['goals_per_90', 'assists_per_90']
            labels = ['Goals / 90', 'Assists / 90']

            fig = go.Figure()
            colors = ['#00e676', '#00b0ff', '#ff007f', '#ffd700', '#7c4dff']
            for i, (idx, row) in enumerate(cmp_df.iterrows()):
                color = colors[i % len(colors)]
                fig.add_trace(go.Bar(
                    x=labels,
                    y=row[stats].values,
                    name=row['name'],
                    marker_color=color,
                    hovertemplate="<b>%{x}</b>: %{y:.2f}<extra>" + row['name'] + "</extra>"
                ))

            fig.update_layout(
                barmode='group',
                paper_bgcolor='#161b22',
                plot_bgcolor='#161b22',
                font=dict(color='#f0f6fc', family='sans-serif'),
                xaxis=dict(showgrid=False, tickfont=dict(color='#c9d1d9', size=12), zeroline=False),
                yaxis=dict(gridcolor='#30363d', tickfont=dict(color='#8b949e'), zerolinecolor='#30363d'),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#f0f6fc'), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=20, t=40, b=40),
                height=360
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            display_df = cmp_df[['name', 'position', 'age_at_season', 'total_minutes',
                                  'actual_value_eur', 'predicted_value_eur']].copy()
            display_df.columns = ['Player', 'Position', 'Age', 'Minutes', 'Actual Value', 'Predicted Value']
            display_df['Actual Value'] = display_df['Actual Value'].apply(lambda x: f'€{x:,.0f}')
            display_df['Predicted Value'] = display_df['Predicted Value'].apply(lambda x: f'€{x:,.0f}')
            st.dataframe(display_df, hide_index=True, use_container_width=True)
    else:
        st.info("Select at least 2 players above to compare.")

# ---------- SEARCH PAGE ----------
elif st.session_state.page == 'search':
    st.subheader("🔍 Player Search")

    all_names = get_all_player_names()
    selected_name = st.selectbox(
        "Search or select player by name",
        options=[""] + all_names,
        index=0,
        placeholder="Type to search player name (e.g. Jamal Musiala, Rodri, Bellingham...)",
        key="search_player_selectbox"
    )

    if not selected_name:
        st.info("Type or select a player name in the search box above to lookup their stats and market value.")
    else:
        search_df = search_players(selected_name)

        if len(search_df) == 0:
            st.info("No players found matching that selection. Try choosing a different name from the list.")
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
                        st.image(season_row['image_url'], width=120)
                    else:
                        st.markdown("<div style='font-size: 80px; text-align: center;'>👤</div>", unsafe_allow_html=True)
                
                with head_c2:
                    st.title(season_row['name'])
                    club_info = season_row['current_club_name'] or "Club N/A"
                    comp_info = f" ({season_row['competition_name']})" if pd.notna(season_row['competition_name']) else ""
                    st.markdown(f"**{season_row['position']}** · Age **{season_row['age_at_season']}** · **{club_info}{comp_info}**")
                    st.caption(f"Season: {season_row['season_year']}")

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
                        st.metric("Value Ratio", f"{ratio:.2f}x", delta=f"Undervalued by €{diff:,.0f}", delta_color="normal")
                    else:
                        st.metric("Value Ratio", f"{ratio:.2f}x", delta=f"Overvalued by €{-diff:,.0f}", delta_color="inverse")

                st.divider()

                st.subheader(f"📊 Per-90 Stats ({season_row['season_year']} Season)")
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

# ---------- INSIGHTS PAGE ----------
elif st.session_state.page == 'insights':
    st.title("📊 Model Insights & Methodology")

    m1, m2, m3 = st.columns(3)
    m1.metric("Model Architecture", "Log-Linear Regression")
    m2.metric("Variance Explained (R²)", "0.57")
    m3.metric("Mean Absolute Error (MAE)", "≈ 0.77 (log scale)")

    st.divider()

    st.subheader("📖 Methodology Summary")
    st.markdown("""
    The transfer market valuation model predicts a player's **logarithmic market value** $\\log(\\text{Market Value})$ 
    using per-90 performance statistics, demographic indicators, and competition tier signals.
    
    - **Target Variable:** $\\log(\\text{Market Value in EUR})$
    - **Input Features:**
      - **Performance (per-90):** `goals_per_90`, `assists_per_90`, `yellows_per_90`, `total_minutes`
      - **Position (one-hot):** `pos_attack`, `pos_midfield`, `pos_defender`, `pos_goalkeeper`
      - **Demographics:** `age_at_season`, `age_squared` (quadratic age curve), `height_in_cm`, `international_caps`
      - **League Quality:** `is_top5_league` (binary flag for Premier League, La Liga, Serie A, Bundesliga, Ligue 1)
    """)

    st.divider()

    st.subheader("🎯 Feature Coefficients")
    st.markdown("Linear regression coefficients on log market value. Positive values increase predicted market value, while negative values penalize it.")

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

    bar_colors = ['#00e676' if v > 0 else '#ff5252' for v in vals]

    fig = go.Figure(go.Bar(
        x=vals,
        y=features,
        orientation='h',
        marker_color=bar_colors,
        text=[f"{v:+.4f}" for v in vals],
        textposition='outside',
        textfont=dict(color='#f0f6fc', size=11, family='sans-serif'),
        hovertemplate="<b>%{y}</b><br>Coefficient: %{x:+.4f}<extra></extra>"
    ))

    fig.update_layout(
        paper_bgcolor='#161b22',
        plot_bgcolor='#161b22',
        font=dict(color='#f0f6fc', family='sans-serif'),
        xaxis=dict(title=dict(text="Coefficient Impact on Log Market Value", font=dict(color='#8b949e', size=12)), gridcolor='#30363d', tickfont=dict(color='#8b949e'), zerolinecolor='#8b949e', zerolinewidth=1.5),
        yaxis=dict(showgrid=False, tickfont=dict(color='#c9d1d9', size=11)),
        margin=dict(l=130, r=60, t=30, b=40),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("⚠️ Known Model Limitations")

    with st.container():
        st.markdown("""
        1. **Absence of Defensive Stats (Tackles, Interceptions, Blocks)**
           - The dataset lacks granular defensive actions (tackles won, interceptions, aerial duels, clearances). 
           - **Impact:** Central defenders, defensive midfielders, and goalkeepers cannot be scored fairly on defensive output. 
           - **Future Improvement:** Integrating **StatsBomb open data** ([hudl/open-data on GitHub](https://github.com/statsbomb/open-data)) as a primary event data source.

        2. **Position-Agnostic Single Age Curve**
           - The model applies a single global quadratic age term (`age` + `age²`), resulting in an estimated peak valuation around **~23 years old**.
           - **Impact:** This peak is unrealistically early for central midfielders, defenders, and goalkeepers who typically reach their prime between ages 27–30.

        3. **Missing Off-Pitch & Contractual Signals**
           - Market valuations in football are heavily driven by factors outside on-pitch box stats.
           - **Impact:** The model lacks signals for **reputation**, **injury history**, **remaining contract length**, and media/hype narratives which strongly influence transfer fees.
        """)
