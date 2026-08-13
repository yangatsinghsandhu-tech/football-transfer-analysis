import duckdb
import os
import pandas as pd
import streamlit as st

def is_valid_db(db_path):
    if not os.path.exists(db_path) or os.path.getsize(db_path) < 10 * 1024 * 1024:
        return False
    try:
        con = duckdb.connect(db_path, read_only=True)
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        con.close()
        return "player_predictions" in tables
    except Exception:
        return False

@st.cache_resource
def get_connection():
    # 1. Check if full valid database exists in repo directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
    repo_db = os.path.join(base_dir, 'transfermarkt-datasets.duckdb')
    
    if is_valid_db(repo_db):
        return duckdb.connect(repo_db, read_only=True)
        
    # 2. Use system temp directory for Streamlit Cloud (always writable)
    temp_dir = tempfile.gettempdir()
    target_db = os.path.join(temp_dir, 'transfermarkt-datasets.duckdb')
    
    # If temp DB is missing or invalid (stale/corrupted), re-assemble from part files
    if not is_valid_db(target_db):
        if os.path.exists(target_db):
            try:
                os.remove(target_db)
            except Exception:
                pass

        part_files = sorted([os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.startswith('transfermarkt-datasets.duckdb.part')])
        if not part_files and os.path.exists('data'):
            part_files = sorted([os.path.join('data', f) for f in os.listdir('data') if f.startswith('transfermarkt-datasets.duckdb.part')])
            
        if part_files:
            tmp_write_path = target_db + '.tmp'
            if os.path.exists(tmp_write_path):
                try:
                    os.remove(tmp_write_path)
                except Exception:
                    pass

            with open(tmp_write_path, 'wb') as f_out:
                for pf in part_files:
                    with open(pf, 'rb') as f_in:
                        f_out.write(f_in.read())
                f_out.flush()
                os.fsync(f_out.fileno())
            
            try:
                os.replace(tmp_write_path, target_db)
            except Exception:
                target_db = tmp_write_path

    if not is_valid_db(target_db) and is_valid_db(repo_db):
        target_db = repo_db

    return duckdb.connect(target_db, read_only=True)

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

