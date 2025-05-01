import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('ChatGPT Analysis of Central Bank Communications')

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
df['announcement_date'] = pd.to_datetime(df['announcement_date'])

return_cols = [col for col in df.columns if col.startswith('T') and col[1:].replace('+', '').replace('-', '').isdigit()]
tickers = sorted(df['ticker'].dropna().unique())

# ---------- SIDEBAR FILTER ----------
st.sidebar.header('Select Market Index')
all_option = 'Select All'
ticker_options = [all_option] + tickers

selected_tickers = st.sidebar.multiselect(
    'Choose tickers to include:',
    options=ticker_options,
    default=tickers[:1]
)

if all_option in selected_tickers or not selected_tickers:
    selected_tickers = tickers

# ---------- FILTER DATA ----------
filtered_df = df[df['ticker'].isin(selected_tickers)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------- PLOTLY SCATTERPLOT ----------
fig1 = px.scatter(
    filtered_df,
    x='announcement_date',
    y='statement_sentiment',
    color='ticker',
    title='GPT Statement Sentiment Over Time',
    hover_data=['ticker', 'statement_sentiment']
)

selected_points = plotly_events(fig1, click_event=True, select_event=False)
st.plotly_chart(fig1)

# ---------- IF A POINT WAS CLICKED ----------
if selected_points:
    selected = selected_points[0]
    clicked_date = pd.to_datetime(selected['x'])

    st.subheader(f"Market Returns Around {clicked_date.date()}")

    df_click = df[(df['announcement_date'] == clicked_date) & (df['ticker'].isin(selected_tickers))]

    if df_click.empty:
        st.info("No return data found for this statement.")
    else:
        returns_melted = df_click.melt(
            id_vars=['ticker'],
            value_vars=return_cols,
            var_name='Day',
            value_name='Return'
        )

        # Optional: Order T-10 to T+10 correctly
        def sort_key(day_str):
            if day_str == 'T0': return 0
            sign = -1 if '-' in day_str else 1
            return sign * int(day_str.replace('T', '').replace('+', '').replace('-', ''))

        returns_melted['Day'] = pd.Categorical(
            returns_melted['Day'],
            categories=sorted(return_cols, key=sort_key),
            ordered=True
        )

        fig2, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=returns_melted, x='Day', y='Return', hue='ticker', marker='o', ax=ax)
        ax.axvline(x='T0', color='red', linestyle='--')
        ax.set_title(f'Returns Surrounding {clicked_date.date()}')
        ax.set_ylabel('Market Return')
        ax.grid(True)
        st.pyplot(fig2)