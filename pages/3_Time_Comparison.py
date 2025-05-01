import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('Time Comparison of Returns and Central Bank Communications')

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

# ---------- COLUMN LOGIC ----------
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
sentiment_cols = [col for col in df.columns if 'sentiment' in col or 'Score' in col]
date_options = pd.to_datetime(df['announcement_date'].dropna().sort_values().unique())
ticker_options = sorted(df['ticker'].dropna().unique())

# ---------- SIDEBAR: Ticker Filter with Select All ----------
st.sidebar.header('Select Market Index/Indices')

all_option = 'Select All'
ticker_options_with_all = [all_option] + ticker_options

selected_tickers_raw = st.sidebar.multiselect(
    'Tickers to display:',
    options=ticker_options_with_all,
    default=ticker_options[:1]
)

if all_option in selected_tickers_raw:
    selected_tickers = ticker_options
else:
    selected_tickers = selected_tickers_raw

# ---------- SLIDER ----------
selected_date = st.select_slider(
    'Select an FOMC Announcement Date:',
    options=list(date_options),
    value=date_options[0],
    format_func=lambda x: x.strftime('%Y-%m-%d')
)

# ---------- FILTER FOR SELECTED DATE & TICKERS ----------
filtered_df = df[(df['announcement_date'] == selected_date) & (df['ticker'].isin(selected_tickers))]

if filtered_df.empty:
    st.warning('No data available for the selected date and tickers.')
    st.stop()

# ---------- PREP FOR PLOTTING ----------
returns_long_format = filtered_df.melt(
    id_vars=['ticker', 'document_type'],
    value_vars=return_cols,
    var_name='Day',
    value_name='Return'
)

def sort_key(day_str):
    if day_str == 'T0':
        return 0
    sign = -1 if '-' in day_str else 1
    return sign * int(day_str.replace('T', '').replace('+', '').replace('-', ''))

returns_long_format['Day'] = pd.Categorical(returns_long_format['Day'], categories=sorted(return_cols, key=sort_key), ordered=True)

# ---------- PLOT ----------
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=returns_long_format, x='Day', y='Return', hue='ticker', marker='o', ax=ax)

ax.axvline(x='T0', color='red', linestyle='--')
announcement_type = filtered_df['document_type'].iloc[0].capitalize()
ax.set_title(f'{announcement_type} on {selected_date.date()} — Market Returns')
ax.set_xlabel('Days from Announcement')
ax.set_ylabel('Return')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ---------- DISPLAY SENTIMENT SCORES ----------
st.subheader('Sentiment Scores for Selected Announcement')

summary = filtered_df[sentiment_cols].mean().to_frame('Sentiment Score') if len(filtered_df) > 1 else filtered_df[sentiment_cols].T.rename(columns={filtered_df.index[0]: 'Sentiment Score'})
summary = summary.round(3)

st.dataframe(summary, use_container_width=False)