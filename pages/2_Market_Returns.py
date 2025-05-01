import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('Market Returns by Index and Document Type')

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
sentiment_cols = [col for col in df.columns if 'Score' in col or 'sentiment' in col]
return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
index_options = sorted(df['ticker'].dropna().unique())
doc_type_options = df['document_type'].dropna().unique()

# ---------- FILTERS ----------
st.sidebar.header('Filters')

all_option = 'Select All'
index_options_with_all = [all_option] + index_options

selected_indices_raw = st.sidebar.multiselect(
    'Select Market Index (multiple allowed)', 
    options=index_options_with_all,
    default=[]
)

selected_indices = index_options if all_option in selected_indices_raw else selected_indices_raw

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

# ---------- VALIDATION ----------
if not selected_indices or not selected_doc_type:
    st.warning('Please select at least one index and one document type.')
    st.stop()

# ---------- FILTER DATA ----------
filtered_data = df[
    (df['ticker'].isin(selected_indices)) &
    (df['document_type'].isin(selected_doc_type))
]

# ---------- CORRELATION HEATMAP ----------
st.subheader('Correlation Heatmap: Sentiment vs. Market Index Returns')
avg_returns_by_ticker = filtered_data.groupby('ticker')[return_cols].mean()
avg_sentiment_by_ticker = filtered_data.groupby('ticker')[sentiment_cols].mean()
merged = avg_sentiment_by_ticker.join(avg_returns_by_ticker)
sentiment_vs_indices = merged[sentiment_cols + return_cols].corr()
sentiment_vs_indices = sentiment_vs_indices.loc[sentiment_cols, return_cols]
sentiment_vs_indices = sentiment_vs_indices.T

fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(
    sentiment_vs_indices,
    annot=True,
    fmt='.3f',
    cmap='coolwarm',
    center=0,
    linewidths=0.3,
    linecolor='black',
    cbar=True,
    ax=ax
)
ax.set_title('Correlation Heatmap: Market Index vs. Sentiment')
plt.xticks(rotation=45)
st.pyplot(fig)


# ---------- AVERAGE RETURN LINE CHART ----------
st.subheader('Average Return by Day Relative to FOMC Announcement')

allowed_types = {'statement', 'intermeeting'}
selected_set = set(selected_doc_type)

def sort_key(day_str):
    if day_str == 'T0':
        return 0
    sign = -1 if '-' in day_str else 1
    return sign * int(day_str.replace('T', '').replace('+', '').replace('-', ''))

sorted_return_cols = sorted(return_cols, key=sort_key)

if selected_set == {'statement'} or selected_set == {'intermeeting'}:
    melted = filtered_data.melt(
        id_vars=['ticker'],
        value_vars=sorted_return_cols,
        var_name='Day',
        value_name='Return'
    )

    fig_line, ax_line = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=melted, x='Day', y='Return', hue='ticker', ci=25, ax=ax_line)

    ax_line.axvline(x='T0', color='red', linestyle='--')
    ax_line.set_title(f'Average Return for {list(selected_set)[0].capitalize()} Days')
    ax_line.set_xlabel('Days from FOMC Announcement')
    ax_line.set_ylabel('Average Return')
    ax_line.grid(True)
    plt.tight_layout()
    st.pyplot(fig_line)

elif selected_set == {'statement', 'intermeeting'}:
    melted = filtered_data.melt(
        id_vars=['document_type'],
        value_vars=sorted_return_cols,
        var_name='Day',
        value_name='Return'
    )

    avg_by_type = melted.groupby(['document_type', 'Day'])['Return'].mean().reset_index()
    avg_by_type['Day'] = pd.Categorical(avg_by_type['Day'], categories=sorted_return_cols, ordered=True)

    fig_line, ax_line = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=avg_by_type, x='Day', y='Return', hue='document_type', ci=25, ax=ax_line)

    ax_line.axvline(x='T0', color='red', linestyle='--')
    ax_line.set_title('Average Return by Day: Statement vs Intermeeting')
    ax_line.set_xlabel('Days from FOMC Announcement')
    ax_line.set_ylabel('Average Return')
    ax_line.grid(True)
    plt.tight_layout()
    st.pyplot(fig_line)

else:
    st.info('This chart only supports analysis of "statement" and/or "intermeeting" document types. Please select only those.')