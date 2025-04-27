import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- FAKE DATA GENERATION ----------
np.random.seed(42)
events = [f'Event {i}' for i in range(1, 101)]
doc_types = np.random.choice(['Statement + Minutes', 'Press Conference'], size=100)

# Simulate returns for SP500, NASDAQ, DJI for -10 to +10 days
returns_cols = [f'{index}_ret({day})' for index in ['SP500', 'NASDAQ', 'DJI'] for day in range(-10, 11)]
returns_data = np.random.randn(100, len(returns_cols)) * 0.01

# Simulate sentiment scores
sentiment_cols = ['ML_sentiment', 'LM_sentiment', 'ChronoBERT_sentiment']
sentiment_data = np.random.randn(100, len(sentiment_cols))

# Create DataFrame
fake_data = pd.DataFrame(
    {
        'Event_ID': events,
        'Doc_Type': doc_types,
        **{col: returns_data[:, idx] for idx, col in enumerate(returns_cols)},
        **{col: sentiment_data[:, idx] for idx, col in enumerate(sentiment_cols)},
    }
)

# ---------- STREAMLIT APP ----------
st.set_page_config(page_title="FED Sentiment Dashboard", layout="wide")
st.title("📈 Market Reactions to Central Bank Communications")

st.markdown("""
Welcome to our demo dashboard! This app visualizes how financial markets react to different types of Federal Reserve communications
using various sentiment analysis methods.

Use the dropdowns to explore different relationships.
""")

# Sidebar Filters
st.sidebar.header("Filters")
selected_sentiment = st.sidebar.selectbox("Select Sentiment Type", sentiment_cols)
selected_index = st.sidebar.selectbox("Select Market Index", ['SP500', 'NASDAQ', 'DJI'])
selected_doc_type = st.sidebar.multiselect("Select Document Type(s)", fake_data['Doc_Type'].unique(), default=fake_data['Doc_Type'].unique())

# Filter data based on selection
filtered_data = fake_data[fake_data['Doc_Type'].isin(selected_doc_type)]

# ---------- CORRELATION TABLE ----------
st.subheader("Correlation between Sentiment and Returns")

corr_cols = [col for col in fake_data.columns if selected_index in col] + sentiment_cols
corr = filtered_data[corr_cols].corr()

st.dataframe(corr.style.background_gradient(cmap='coolwarm', axis=None))

# ---------- SCATTERPLOT ----------
st.subheader("Scatterplot: Returns vs Sentiment")

selected_day = st.slider("Select Day Relative to Announcement", -10, 10, 0)
ret_col = f'{selected_index}_ret({selected_day})'

fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x=selected_sentiment, y=ret_col, hue='Doc_Type', ax=ax)
plt.title(f'{ret_col} vs {selected_sentiment}')
plt.xlabel(selected_sentiment)
plt.ylabel(f'{selected_index} Return (Day {selected_day})')
st.pyplot(fig)

# ---------- BOXPLOT ----------
st.subheader("Boxplot: Returns by Document Type")

fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_data, x='Doc_Type', y=ret_col)
plt.title(f'{ret_col} Distribution by Document Type')
plt.xlabel("Document Type")
plt.ylabel(f'{selected_index} Return (Day {selected_day})')
st.pyplot(fig2)

# ---------- CONCLUSIONS SECTION ----------
st.subheader("Conclusions")
st.markdown("""
In the final version of this dashboard, we'll replace this fake data with our real collected data and draw conclusions
based on actual relationships observed.
""")

# ---------- END ----------
