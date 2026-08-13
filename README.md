# ⚽ Football Moneyball — Transfer Market Value Model

An interactive Streamlit analytics application identifying **undervalued football players** across European leagues by evaluating per-90 performance metrics against model-predicted transfer market valuations.

![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-00e676?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-0.9+-yellow?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple?style=flat-square&logo=plotly)

---

## 🌟 Key Features

- **📉 Undervalued Player Discovery**: Search and rank player listings by valuation ratio ($\text{Predicted Market Value} / \text{Actual Market Value}$).
- **⚖️ Head-to-Head Player Comparison**: Interactive multi-bar Plotly charts comparing per-90 goals, assists, total minutes, and market values across seasons.
- **🔍 Player Lookup & Autocomplete Search**: Real-time autocomplete name search across **40,684 records** covering **2018–2026** seasons.
- **📊 Model Methodology & Insights**: Interactive Plotly coefficient bar chart breaking down linear regression model feature weights ($R^2 = 0.57$, MAE $\approx 0.77$).
- **🎨 Fotmob-Inspired Dark UI**: Custom dark theme palette, pill-tab navigation, 3D hover-lift card containers, and animated count-up metrics.

---

## 🚀 Deploying to Streamlit Community Cloud (Free Hosting & Shareable Link)

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

Streamlit Cloud will automatically install dependencies from `requirements.txt`, auto-rejoin the database parts on first launch, and host your app on a shareable link (e.g. `https://football-transfer-analysis.streamlit.app`).

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
│   └── config.toml             # Global Fotmob dark theme palette
├── dashboard/
│   ├── .streamlit/
│   │   └── config.toml         # Dashboard-level Streamlit theme configuration
│   ├── app.py                  # Main Streamlit dashboard application (single-file button routing)
│   └── utils/
│       └── data.py             # DuckDB connection, cached data queries, split-DB auto-rejoin
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

## 📄 License & Attribution

Data sourced from Transfermarkt datasets. Built with Python, Streamlit, DuckDB, and Plotly.
