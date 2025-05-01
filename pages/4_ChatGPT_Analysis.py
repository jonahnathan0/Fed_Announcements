import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('ChatGPT Analysis of Central Bank Communications')

# ------------------ CUSTOM STYLE ------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #1f2937;
        }

        /* Sidebar text color only (keep default font) */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Keep default font across body */
        html, body, [class*="css"] {
            color: #1f2937 !important;
        }

        /* Header styling (no font override) */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700 !important;
            color: #1f2937 !important;
        }

        /* Link color */
        a {
            color: #2563eb !important;
            text-decoration: none;
        }

        /* Button styling (no font override) */
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 6px;
            padding: 0.4em 1em;
            font-weight: bold;
        }

        /* Dropdown label */
        .stSelectbox label {
            font-weight: bold;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_csv('raw_data/final_dataset.csv')
df['announcement_date'] = pd.to_datetime(df['announcement_date'])

return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
tickers = sorted(df['ticker'].dropna().unique())

# ---------- SIDEBAR: Ticker Selection ----------
st.sidebar.header('Select Market Index')
all_option = 'Select All'
ticker_options = [all_option] + tickers

selected_tickers = st.sidebar.multiselect(
    'Choose tickers to include:',
    options=ticker_options,
    default=tickers[:1]
)

if all_option in selected_tickers or not selected_tickers:
    selected_tickers = tickers

# ---------- SLIDER: Announcement Date ----------
date_options = sorted(df['announcement_date'].dropna().unique())
selected_date = st.select_slider(
    'Select an FOMC Announcement Date:',
    options=list(date_options),
    value=date_options[0],
    format_func=lambda x: pd.to_datetime(x).strftime('%Y-%m-%d')
)

# ---------- FILTER DATA ----------
filtered_df = df[(df['announcement_date'] == selected_date) & (df['ticker'].isin(selected_tickers))]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------- GET DOCUMENT TYPE ----------
announcement_type = filtered_df['document_type'].iloc[0].lower()
sentiment_column = 'statement_sentiment' if announcement_type == 'statement' else 'intermeeting_sentiment'

# ---------- SCATTER PLOT ----------
st.subheader(f"{announcement_type.title()} Sentiment vs Market Returns")

fig, ax = plt.subplots(figsize=(14, 6))

for ret_col in return_cols:
    sns.scatterplot(
        data=filtered_df,
        x=sentiment_column,
        y=ret_col,
        label=ret_col,
        ax=ax
    )

ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.axvline(0, color='gray', linestyle='--', linewidth=1)
ax.set_xlabel('GPT Sentiment Score')
ax.set_ylabel('Market Return')
ax.set_title(f'{announcement_type.title()} on {selected_date.date()} — Market Returns')
ax.legend(
    title='Return Period',
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0,
    frameon=True
)
ax.grid(True)
st.pyplot(fig)