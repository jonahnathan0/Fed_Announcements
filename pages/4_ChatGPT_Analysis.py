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

        /* Always show dropdown arrow on multiselect */
        div[data-baseweb="select"] > div {
            background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 10l5 5 5-5' stroke='%232563eb' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1rem;
        }

        /* Ensure space for arrow in multiselect input */
        div[data-baseweb="select"] > div > div {
            padding-right: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_csv('raw_data/final_dataset.csv')
df['announcement_date'] = pd.to_datetime(df['announcement_date'])

# ---------- SETUP ----------
tickers = sorted(df['ticker'].dropna().unique())

# ---------- SIDEBAR: Ticker Filter ----------
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

# ---------- FILTER DATA ----------
filtered_df = df[df['ticker'].isin(selected_tickers)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------- SCATTERPLOT ----------
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(
    data=filtered_df,
    x='announcement_date',
    y='statement_sentiment',
    hue='ticker',
    s=60,
    ax=ax
)

ax.set_title('GPT Statement Sentiment Over Time')
ax.set_xlabel('Announcement Date')
ax.set_ylabel('Statement Sentiment Score')
ax.grid(True)
ax.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)