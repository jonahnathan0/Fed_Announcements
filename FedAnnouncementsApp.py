import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG & DATA ----------
st.set_page_config(page_title='FED Sentiment Dashboard', layout='wide')
df = pd.read_csv('raw_data/final_dataset.csv')

sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())
doc_type_options = df['document_type'].dropna().unique()

# ---------- TITLE & INTRO ----------
st.title('Market Reactions to FED Announcements')

st.markdown('''
This app shows how financial markets react to different types of Federal Reserve communications
using various sentiment analysis methods. Use the dropdowns to explore different relationships.
''')

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header('Filters')

all_option = 'Select All'
index_options_with_all = [all_option] + index_options

selected_indices_raw = st.sidebar.multiselect(
    'Select Market Index (multiple allowed)', 
    options=index_options_with_all,
    default=[]
)

if all_option in selected_indices_raw:
    selected_indices = index_options
else:
    selected_indices = selected_indices_raw

doc_all_option = 'Select All'
doc_type_options_with_all = [doc_all_option] + list(doc_type_options)

selected_doc_type_raw = st.sidebar.multiselect(
    'Select Document Type(s)',
    options=doc_type_options_with_all,
    default=[]
)

selected_doc_type = [doc for doc in selected_doc_type_raw if doc != doc_all_option]
if not selected_doc_type:
    selected_doc_type = list(doc_type_options)

# ---------- SPLASH SCREEN ----------
if not selected_indices or not selected_doc_type:
    st.image('assets/Banking-December-FOMC-announcement-live-blog.jpg', use_container_width=True)
    st.markdown('Use the filters on the left to get started.')
    st.stop()

# ---------- FILTERED DATA ----------
filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

# ---------- CORRELATION HEATMAP ----------
st.subheader('Correlation Heatmap: Sentiment vs. Market Returns')

corr_matrix = filtered_data[sentiment_cols + return_cols].corr()
sentiment_vs_returns = corr_matrix.loc[sentiment_cols, return_cols]

fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(
    sentiment_vs_returns,
    annot=True,
    fmt='.3f',
    cmap='coolwarm',
    center=0,
    linewidths=0.3,
    linecolor='black',
    cbar=True,
    ax=ax
)
title_label = ', '.join(selected_indices)
ax.set_title(f'Correlation: {title_label} - Sentiment vs. Market Returns', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------- AVERAGE RETURN LINE CHART ----------
st.subheader('Average Return by Day Relative to FOMC Announcement')

allowed_types = {'statement', 'intermeeting'}
selected_set = set(selected_doc_type)

if selected_set == {'statement'} or selected_set == {'intermeeting'}:
    # Single type selected — plot one line
    melted = filtered_data.melt(
        id_vars=['ticker'],
        value_vars=return_cols,
        var_name='Day',
        value_name='Return'
    )
    melted['Day'] = melted['Day'].str.replace('T', '').astype(int)

    fig_line, ax_line = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=melted, x='Day', y='Return', hue='ticker', ax=ax_line)

    ax_line.axvline(0, color='red', linestyle='--')
    ax_line.set_title(f'Average Return for {list(selected_set)[0].capitalize()} Days')
    ax_line.set_xlabel('Days from FOMC Announcement')
    ax_line.set_ylabel('Average Return')
    ax_line.grid(True)
    plt.tight_layout()
    st.pyplot(fig_line)

elif selected_set == {'statement', 'intermeeting'}:
    # Both types selected — plot two lines grouped by document_type
    melted = filtered_data.melt(
        id_vars=['document_type'],
        value_vars=return_cols,
        var_name='Day',
        value_name='Return'
    )
    melted['Day'] = melted['Day'].str.replace('T', '').astype(int)

    avg_by_type = melted.groupby(['document_type', 'Day'])['Return'].mean().reset_index()

    fig_line, ax_line = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=avg_by_type, x='Day', y='Return', hue='document_type', ax=ax_line)

    ax_line.axvline(0, color='red', linestyle='--')
    ax_line.set_title('Average Return by Day: Statement vs Intermeeting')
    ax_line.set_xlabel('Days from FOMC Announcement')
    ax_line.set_ylabel('Average Return')
    ax_line.grid(True)
    plt.tight_layout()
    st.pyplot(fig_line)

else:
    # Invalid selection (includes press conferences or anything else)
    st.info('This chart only supports analysis of "statement" and/or "intermeeting" document types. Please select only those.')

# ---------- CONCLUSIONS ----------
st.subheader('Conclusions')
st.markdown('''
This dashboard shows how different sentiment signals relate to market performance around FOMC announcements.
Explore different indexes, document types, and sentiment models to uncover patterns in how the market reacts.
''')