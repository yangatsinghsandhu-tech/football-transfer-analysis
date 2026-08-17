# Football Moneyball — Transfer Market Valuation & Scouting System

An interactive Streamlit quantitative analytics application identifying **undervalued football players** across European leagues by evaluating per-90 performance metrics against statistical model valuations.

[![Live App](https://img.shields.io/badge/Live_App-Streamlit_Cloud-10b981?style=for-the-badge&logo=streamlit)](https://football-transfer-analysis-cutahstypfgimy3bc4bj4k.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-0.9+-yellow?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple?style=flat-square&logo=plotly)

🔗 **Live Web Application**: [https://football-transfer-analysis-cutahstypfgimy3bc4bj4k.streamlit.app/](https://football-transfer-analysis-cutahstypfgimy3bc4bj4k.streamlit.app/)

---

## 🌟 Key System Features

- **Undervalued Asset Discovery Index**: Search and rank player listings by valuation ratio ($\text{Valuation Ratio} = \frac{\text{Predicted Market Value}}{\text{Actual Market Value}}$).
- **Head-to-Head Player Comparison**: Multi-metric Plotly grouped bar overlays comparing per-90 goals, assists, total minutes, and market values across seasons.
- **Player Lookup & Autocomplete Search**: Real-time autocomplete name search across **40,684 records** covering **2018–2026** seasons.
- **Model Architecture & Coefficients**: Interactive Plotly horizontal feature impact chart detailing linear regression weights ($R^2 = 0.57$, MAE $\approx 0.77$).
- **Grounded Tactical UI/UX**: Professional pitch-slate theme (`#0b0f17`), IBM Plex Sans & Barlow typography, asymmetrical scouting dashboard, skeleton loading indicators, and built-in Terms of Service / Privacy Policy legal dialogs.
- **Resilient Cloud Data Pipeline**: Automatic split-database reassembly (`part1`, `part2`, `part3`) with `/tmp` directory fallback and catalog validation for 100% reliable execution on Streamlit Cloud.

---

## 🚀 Deploying to Streamlit Community Cloud (Free Hosting)

You can host this application live for free on [Streamlit Community Cloud](https://streamlit.io/cloud) in under 2 minutes:

1. **Push Repository to GitHub**:
   Ensure this repository is committed and pushed to your GitHub profile (`https://github.com/yangatsinghsandhu-tech/football-transfer-analysis`).
2. **Sign In to Streamlit Cloud**:
   Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account (`yangatsinghsandhu-tech`).
3. **Deploy New App**:
   - Click **Create App** / **New App**.
   - Select Repository: `yangatsinghsandhu-tech/football-transfer-analysis`.
   - Select Branch: `main` (or `master`).
   - Set **Main file path**: `dashboard/app.py`.
   - Click **Deploy!**

Streamlit Cloud automatically installs dependencies from `requirements.txt`, auto-assembles split database parts in the system `/tmp` directory, and hosts your app on a shareable link (e.g. `https://football-transfer-analysis.streamlit.app`).

---

## 💻 Local Setup & Execution

### Prerequisites
- Python 3.10+

### Installation & Run

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yangatsinghsandhu-tech/football-transfer-analysis.git
   cd football-transfer-analysis
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```
football_transfer_analysis/
├── .streamlit/
│   └── config.toml             # Grounded dark slate theme palette (#0b0f17)
├── dashboard/
│   ├── .streamlit/
│   │   └── config.toml         # App-level Streamlit theme configuration
│   ├── app.py                  # Streamlit dashboard application (single-file routing & dialogs)
│   └── utils/
│       └── data.py             # DuckDB connection, catalog validation, split-DB auto-rejoin
├── data/
│   ├── transfermarkt-datasets.duckdb.part1  # Split DuckDB part 1 (<70MB for GitHub limits)
│   ├── transfermarkt-datasets.duckdb.part2  # Split DuckDB part 2
│   ├── transfermarkt-datasets.duckdb.part3  # Split DuckDB part 3
│   └── undervalued_players_v1.csv
├── models/
│   ├── features_v5.pkl
│   └── transfer_value_model_v5.pkl
├── notebooks/
│   └── 01_ingestion.ipynb
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📄 License & Legal Attribution

- **Data Sources**: Transfermarkt Public Datasets & StatsBomb Open Data repositories.
- **Terms & Privacy**: Legal disclaimers and privacy guidelines integrated directly via in-app dialog modals.
