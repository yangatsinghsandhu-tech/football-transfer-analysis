import duckdb
import os
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/transfermarkt-datasets.duckdb'))
    
    if not os.path.exists(db_path) or os.path.getsize(db_path) < 10 * 1024 * 1024:
        data_dir = os.path.dirname(db_path)
        if not os.path.exists(data_dir):
            data_dir = os.path.abspath('data')
            
        if os.path.exists(data_dir):
            part_files = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith('transfermarkt-datasets.duckdb.part')])
            if part_files:
                tmp_path = db_path + '.tmp'
                with open(tmp_path, 'wb') as f_out:
                    for pf in part_files:
                        with open(pf, 'rb') as f_in:
                            f_out.write(f_in.read())
                    f_out.flush()
                    os.fsync(f_out.fileno())
                
                if os.path.exists(db_path):
                    try:
                        os.remove(db_path)
                    except Exception:
                        pass
                try:
                    os.replace(tmp_path, db_path)
                except Exception:
                    if os.path.exists(tmp_path):
                        db_path = tmp_path

    if not os.path.exists(db_path):
        db_path = os.path.abspath('data/transfermarkt-datasets.duckdb')
    return duckdb.connect(db_path, read_only=True)

@st.cache_data
def load_undervalued(season=2025, positions=None):
    con = get_connection()
    pos_filter = ""
    if positions:
        pos_list = "', '".join(positions)
        pos_filter = f"AND position IN ('{pos_list}')"
    query = f"""
        SELECT name, position, age_at_season, goals_per_90, assists_per_90,
               total_minutes, actual_value_eur, predicted_value_eur, value_ratio
        FROM player_predictions
        WHERE season_year = {season} {pos_filter}
        ORDER BY residual ASC
    """
    return con.execute(query).df()

@st.cache_data
def load_photos(names):
    if not names:
        return pd.DataFrame(columns=['name', 'image_url'])
    con = get_connection()
    placeholders = ", ".join(["?"] * len(names))
    query = f"""
        SELECT name, image_url
        FROM (
            SELECT name, image_url,
                   ROW_NUMBER() OVER (PARTITION BY name ORDER BY market_value_in_eur DESC NULLS LAST, player_id DESC) as rn
            FROM players
            WHERE name IN ({placeholders})
        ) sub
        WHERE rn = 1
    """
    df = con.execute(query, names).df()
    return df.drop_duplicates(subset='name', keep='first')

@st.cache_data
def search_players(search_query):
    if not search_query or not search_query.strip():
        return pd.DataFrame()
    con = get_connection()
    query = """
        SELECT pp.*, p.image_url, p.current_club_name, c.name as competition_name
        FROM player_predictions pp
        LEFT JOIN players p ON pp.player_id = p.player_id
        LEFT JOIN competitions c ON p.current_club_domestic_competition_id = c.competition_id
        WHERE pp.name ILIKE ?
        ORDER BY pp.name, pp.season_year DESC
    """
    df = con.execute(query, [f"%{search_query.strip()}%"]).df()
    return df

@st.cache_data
def get_all_player_names():
    con = get_connection()
    return con.execute("SELECT DISTINCT name FROM player_predictions ORDER BY name").df()['name'].tolist()

@st.cache_data
def load_compare_players(selected_players, season):
    if not selected_players or len(selected_players) < 2:
        return pd.DataFrame()
    con = get_connection()
    placeholders = ", ".join(["?"] * len(selected_players))
    query = f"""
        SELECT name, position, age_at_season, goals_per_90, assists_per_90,
               total_minutes, actual_value_eur, predicted_value_eur
        FROM player_predictions
        WHERE name IN ({placeholders}) AND season_year = ?
    """
    df = con.execute(query, selected_players + [season]).df()
    return df.drop_duplicates(subset='name')

