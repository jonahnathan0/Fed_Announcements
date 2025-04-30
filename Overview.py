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

FILL IN

## Introduction

FILL IN

## Overview

FILL IN

---
''')