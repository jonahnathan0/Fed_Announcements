import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ------------------ PAGE CONFIG (Must Be First) ------------------
st.set_page_config(
    page_title='FED Sentiment Dashboard',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ------------------ CUSTOM STYLE -------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #1f2937;
        }

        /* Sidebar text color only */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Force main text color globally */
        .block-container, .main, .element-container, body, html {
            color: #111111 !important;
        }

        /* Override for dark mode manually (Streamlit doesn't respect media queries well) */
        html[data-theme="dark"] .block-container,
        html[data-theme="dark"] .main,
        html[data-theme="dark"] .element-container,
        html[data-theme="dark"] body {
            color: #ffffff !important;
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700 !important;
            color: inherit !important;
        }

        /* Link color */
        a {
            color: #2563eb !important;
            text-decoration: none;
        }

        /* Button styling */
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
    </style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR NAV ------------------
with st.sidebar:
    st.markdown('## Navigation')
    st.markdown('Use the sidebar above to switch between sections of the dashboard.')
    st.markdown('[Fed Announcements Project Repo](https://github.com/jonahnathan0/Fed_Announcements)')

# ------------------ OVERVIEW ------------------
st.title('Market Reactions to Central Bank Communications')

# Display image at the top and center it
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image('assets/Banking-December-FOMC-announcement-live-blog.jpg', width=1000)

st.markdown('''
## Project Context

Monetary policy decisions made from central banks, specifically the US Federal Reserve (Fed), are some of the most closely watched events in financial markets. Whether it’s a change in interest rates, commentary on economic conditions, or possibly even forward guidance on future tightening or easing of rates, the language used by the Federal Open Market Committee (FOMC) can influence billions of dollars in assets.

## Introduction

Our project investigated how financial markets respond to Fed communications through a sentiment analysis of FOMC announcements. Since Fed communications can significantly impact financial markets, the sentiment from these announcements can provide valuable insights to market participants. Using various language dictionaries to monitor sentiment of the announcements, we were able to compare that sentiment to real returns of stock indices at the time of the announcements. Also, by using OpenAI API with GPT-4, we created a prompt that outputted the bearishness or bullishness of the announcement.

## Links to Data and Inputs
- [FOMC Historical Transcripts](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm)
- [Yahoo Finance Python](https://pypi.org/project/yfinance/)
- [Yahoo Finance Historical Data on Indicies](https://finance.yahoo.com/)
- [LM Dictionary](https://github.com/jonahnathan0/Fed_Announcements/blob/main/inputs/LM_MasterDictionary_1993-2021.csv)
- [ML Negative Dictionary](https://github.com/jonahnathan0/Fed_Announcements/blob/main/inputs/ML_negative_unigram.txt)
- [ML Positive Dictionary](https://github.com/jonahnathan0/Fed_Announcements/blob/main/inputs/ML_positive_unigram.txt)

---
''')