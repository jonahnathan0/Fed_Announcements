import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ------------------ PAGE CONFIG (Must Be First) ------------------
st.set_page_config(
    page_title='FED Sentiment Dashboard',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ------------------ CUSTOM CSS STYLE ------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #1f2937; /* Dark blue-gray */
        }

        /* Force all sidebar text to white and use Calibri */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
            font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif !important;
        }

        /* Universal font and color for entire app */
        html, body, [class*="css"] {
            font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif !important;
            color: #1f2937 !important;
        }

        /* All headers same font + weight */
        h1, h2, h3, h4, h5, h6 {
            font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif !important;
            font-weight: 700 !important;
            color: #1f2937 !important;
        }

        /* Links color */
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
            font-family: Calibri, Candara, Segoe, Segoe UI, Optima, Arial, sans-serif !important;
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
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image('assets/Banking-December-FOMC-announcement-live-blog.jpg', width=800)

st.markdown('''
## Project Context

FILL IN

## Introduction

FILL IN

## Overview

FILL IN

---
''')