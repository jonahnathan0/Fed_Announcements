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

# ---------- SLIDER ----------
selected_date = st.select_slider(
    'Select an FOMC Announcement Date:',
    options=list(date_options),
    value=date_options[0],
    format_func=lambda x: x.strftime('%Y-%m-%d')
)

# ---------- FILTER FOR SELECTED DATE ----------
selected_row = df[df['announcement_date'] == selected_date]

if selected_row.empty:
    st.warning('No data available for the selected date.')
    st.stop()

# ---------- EXTRACT INFO ----------
selected_type = selected_row['document_type'].values[0]
selected_ticker = selected_row['ticker'].values[0]

# ---------- PREP FOR PLOTTING ----------
melted = selected_row.melt(
    value_vars=return_cols,
    var_name='Day',
    value_name='Return'
)

def sort_key(day_str):
    if day_str == 'T0':
        return 0
    sign = -1 if '-' in day_str else 1
    return sign * int(day_str.replace('T', '').replace('+', '').replace('-', ''))

melted['Day'] = pd.Categorical(melted['Day'], categories=sorted(return_cols, key=sort_key), ordered=True)

# ---------- PLOT ----------
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=melted, x='Day', y='Return', marker='o', ax=ax)

ax.axvline(x='T0', color='red', linestyle='--')
ax.set_title(f'{selected_type.capitalize()} on {selected_date.date()} — Returns for {selected_ticker}')
ax.set_xlabel('Days from Announcement')
ax.set_ylabel('Return')
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)