import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- REAL DATA ----------
st.set_page_config(page_title="FED Sentiment Dashboard", layout="wide")
df = pd.read_csv("raw_data/final_dataset.csv")

sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].lstrip('+-').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())

# ---------- STREAMLIT UI ----------
st.title("📈 Market Reactions to Central Bank Communications")

st.markdown("""
Welcome to our dashboard! This app visualizes how financial markets react to different types of Federal Reserve communications
using various sentiment analysis methods.

Use the dropdowns to explore different relationships.
""")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

# Index multi-select with Select All
select_all_indices = st.sidebar.checkbox("Select All Indices", value=True)
if select_all_indices:
    selected_indices = index_options
else:
    selected_indices = st.sidebar.multiselect("Select Market Index (you can select multiple)", index_options)

# Document type multi-select
selected_doc_type = st.sidebar.multiselect(
    "Select Document Type(s)",
    df['document_type'].dropna().unique(),
    default=df['document_type'].dropna().unique()
)

# ---------- FILTER DATA ----------
filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

# ---------- CORRELATION HEATMAP ----------
st.subheader("Correlation between Sentiment and Returns")

corr_cols = sentiment_cols + return_cols
corr = filtered_data[corr_cols].corr().loc[sentiment_cols, return_cols]
st.dataframe(corr.style.background_gradient(cmap='coolwarm', axis=None))

# ---------- SCATTERPLOT ----------
st.subheader("Scatterplot: Returns vs Sentiment")

selected_day = st.slider("Select Day Relative to Announcement", -10, 10, 0)
ret_col = f'T{selected_day}' if selected_day != 0 else 'T0'

fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x=selected_sentiment, y=ret_col, hue='document_type', ax=ax)

title_index_label = (
    "Multiple Indices" if len(selected_indices) > 1 else selected_indices[0]
)
plt.title(f'{ret_col} vs {selected_sentiment} for {title_index_label}')
plt.xlabel(selected_sentiment)
plt.ylabel(f'{title_index_label} Return (Day {selected_day})')
st.pyplot(fig)

# ---------- BOXPLOT ----------
st.subheader("Boxplot: Returns by Document Type")

fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_data, x='document_type', y=ret_col)
plt.title(f'{ret_col} Distribution by Document Type')
plt.xlabel("Document Type")
plt.ylabel(f'{title_index_label} Return (Day {selected_day})')
st.pyplot(fig2)

# ---------- CONCLUSIONS SECTION ----------
st.subheader("Conclusions")
st.markdown("""
This dashboard shows how different sentiment signals relate to market performance around FOMC announcements.
Explore different indexes, document types, and sentiment models to uncover patterns in how the market reacts.
""")
