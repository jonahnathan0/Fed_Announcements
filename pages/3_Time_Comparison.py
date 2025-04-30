import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('Time Comparison of Returns and Central Bank Communications')

# ---------- LOAD DATA ----------
df = pd.read_csv('raw_data/final_dataset.csv')
df['announcement_date'] = pd.to_datetime(df['announcement_date'])

# ---------- COLUMN LOGIC ----------
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
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