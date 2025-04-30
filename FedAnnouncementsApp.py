import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- REAL DATA ----------
st.set_page_config(page_title="FED Sentiment Dashboard", layout="wide")
df = pd.read_csv("raw_data/final_dataset.csv")

# Identify columns
sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())
doc_type_options = df['document_type'].dropna().unique()

# ---------- STREAMLIT UI ----------
st.title("📈 Market Reactions to Central Bank Communications")

st.markdown("""
Welcome to our dashboard! This app visualizes how financial markets react to different types of Federal Reserve communications
using various sentiment analysis methods.

Use the dropdowns to explore different relationships.
""")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

# Select All Indices + Multiselect
select_all_indices = st.sidebar.checkbox("Select All Indices", value=True)
if select_all_indices:
    selected_indices = index_options
else:
    selected_indices = st.sidebar.multiselect("Select Market Index (multiple allowed)", options=index_options, default=index_options[:1])

# Document type multiselect
selected_doc_type = st.sidebar.multiselect(
    "Select Document Type(s)",
    options=doc_type_options,
    default=doc_type_options
)

# ---------- FILTER DATA ----------
filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

# ---------- CORRELATION HEATMAP ----------
st.subheader("Correlation Heatmap: Sentiment vs. Market Returns")

# Calculate correlation
corr_matrix = filtered_data[sentiment_cols + return_cols].corr()
sentiment_vs_returns = corr_matrix.loc[sentiment_cols, return_cols]

# Plot heatmap
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
title_label = "All Indices" if len(selected_indices) == len(index_options) else ", ".join(selected_indices)
ax.set_title(f"Correlation: {title_label} - Sentiment vs. Market Returns", fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------- CONCLUSIONS SECTION ----------
st.subheader("Conclusions")
st.markdown("""
This dashboard shows how different sentiment signals relate to market performance around FOMC announcements.
Explore different indexes, document types, and sentiment models to uncover patterns in how the market reacts.
""")
