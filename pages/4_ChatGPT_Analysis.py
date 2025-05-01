import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import matplotlib.pyplot as plt
import seaborn as sns

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

return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
tickers = sorted(df['ticker'].dropna().unique())

# ---------- SENTIMENT BINNING ----------
def sentiment_category(score):
    if score > 0.2:
        return 'Bullish'
    elif score < -0.2:
        return 'Bearish'
    else:
        return 'Neutral'

df['sentiment_bin'] = df['statement_sentiment'].apply(sentiment_category)

# ---------- MELT TO LONG FORMAT ----------
df_melted = df.melt(
    id_vars=['announcement_date', 'sentiment_bin'],
    value_vars=return_cols,
    var_name='Day',
    value_name='Return'
)

# ---------- SORT DAY CATEGORIES ----------
def sort_key(day):
    if day == 'T0':
        return 0
    sign = -1 if '-' in day else 1
    return sign * int(day.replace('T', '').replace('+', '').replace('-', ''))

df_melted['Day'] = pd.Categorical(
    df_melted['Day'],
    categories=sorted(return_cols, key=sort_key),
    ordered=True
)

# ---------- COMPUTE AVERAGE RETURNS ----------
grouped_returns = df_melted.groupby(['Day', 'sentiment_bin'])['Return'].mean().reset_index()

# ---------- PLOT ----------
st.markdown('## Average Return Curve by Sentiment')
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=grouped_returns, x='Day', y='Return', hue='sentiment_bin', marker='o', ax=ax)
ax.axhline(0, color='gray', linestyle='--')
ax.set_title("Average Market Return by Sentiment Bin Across Days")
ax.set_xlabel("Relative Day from Announcement")
ax.set_ylabel("Average Return")
ax.grid(True)
st.pyplot(fig)