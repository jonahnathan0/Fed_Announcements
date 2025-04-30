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

# Sidebar Filters
st.sidebar.header("Filters")
selected_sentiment = st.sidebar.selectbox("Select Sentiment Type", sentiment_cols)
selected_index = st.sidebar.selectbox("Select Market Index", index_options)
selected_doc_type = st.sidebar.multiselect("Select Document Type(s)", df['document_type'].dropna().unique(), default=df['document_type'].dropna().unique())

# Filter data based on selection
filtered_data = df[(df['ticker'] == selected_index) & (df['document_type'].isin(selected_doc_type))]

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
plt.title(f'{ret_col} vs {selected_sentiment} for {selected_index}')
plt.xlabel(selected_sentiment)
plt.ylabel(f'{selected_index} Return (Day {selected_day})')
st.pyplot(fig)

# ---------- BOXPLOT ----------
st.subheader("Boxplot: Returns by Document Type")

fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_data, x='document_type', y=ret_col)
plt.title(f'{ret_col} Distribution by Document Type')
plt.xlabel("Document Type")
plt.ylabel(f'{selected_index} Return (Day {selected_day})')
st.pyplot(fig2)

# ---------- CONCLUSIONS SECTION ----------
st.subheader("Conclusions")
st.markdown("""
This dashboard shows how different sentiment signals relate to market performance around FOMC announcements.
Explore different indexes, document types, and sentiment models to uncover patterns in how the market reacts.
""")
