import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title='Market Returns', layout='wide')
st.title('📊 Market Returns by Index and Document Type')

df = pd.read_csv('raw_data/final_dataset.csv')
sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())
doc_type_options = df['document_type'].dropna().unique()

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

if not selected_indices or not selected_doc_type:
    st.warning('Please select at least one index and one document type.')
    st.stop()

filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

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
ax.set_title('Correlation Heatmap')
plt.xticks(rotation=45)
st.pyplot(fig)
