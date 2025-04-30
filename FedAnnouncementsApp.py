import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG & DATA ----------
st.set_page_config(page_title="FED Sentiment Dashboard", layout="wide")
df = pd.read_csv("raw_data/final_dataset.csv")

sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())
doc_type_options = df['document_type'].dropna().unique()

# ---------- TITLE & INTRO ----------
st.title("Market Reactions to FED Announcements")

st.markdown("""
This app shows how financial markets react to different types of Federal Reserve communications
using various sentiment analysis methods.

Use the dropdowns to explore different relationships.
""")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

all_option = "Select All"
index_options_with_all = [all_option] + index_options

selected_indices_raw = st.sidebar.multiselect(
    "Select Market Index (multiple allowed)", 
    options=index_options_with_all,
    default=[]
)

if all_option in selected_indices_raw:
    selected_indices = index_options
else:
    selected_indices = selected_indices_raw

doc_all_option = "Select All"
doc_type_options_with_all = [doc_all_option] + list(doc_type_options)

selected_doc_type_raw = st.sidebar.multiselect(
    "Select Document Type(s)",
    options=doc_type_options_with_all,
    default=[]
)

if doc_all_option in selected_doc_type_raw:
    selected_doc_type = list(doc_type_options)
else:
    selected_doc_type = selected_doc_type_raw

# ---------- SPLASH SCREEN ----------
if not selected_indices or not selected_doc_type:
    st.image("assets/Banking-December-FOMC-announcement-live-blog.jpg", use_container_width=True)
    st.markdown("Use the filters on the left to get started.")
    st.stop()

# ---------- FILTERED DATA ----------
filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

# ---------- CORRELATION HEATMAP ----------
st.subheader("Correlation Heatmap: Sentiment vs. Market Returns")

corr_matrix = filtered_data[sentiment_cols + return_cols].corr()
sentiment_vs_returns = corr_matrix.loc[sentiment_cols, return_cols]

fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(
    sentiment_vs_returns,
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    center=0,
    linewidths=0.3,
    linecolor='black',
    cbar=True,
    ax=ax
)
title_label = ", ".join(selected_indices)
ax.set_title(f"Correlation: {title_label} - Sentiment vs. Market Returns", fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------- CONCLUSIONS ----------
st.subheader("Conclusions")
st.markdown("""
This dashboard shows how different sentiment signals relate to market performance around FOMC announcements.
Explore different indexes, document types, and sentiment models to uncover patterns in how the market reacts.
""")