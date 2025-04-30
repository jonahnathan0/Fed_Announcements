import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title='FED Sentiment Dashboard',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ------------------ SIDEBAR NAV ------------------
with st.sidebar:
    st.markdown('## Navigation')
    st.markdown('Use the sidebar above to switch between sections of the dashboard.')
    st.markdown('[Fed Announcements Project Repo](https://github.com/jonahnathan0/Fed_Announcements)')

# ------------------ OVERVIEW ------------------
st.title('Market Reactions to Central Bank Communications')

# Display image at the top
st.markdown(
    """
    <div style="text-align: center;">
        <img src="assets/Banking-December-FOMC-announcement-live-blog.jpg" width="500"/>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('''
## Project Context

FILL IN

## Introduction

FILL IN

## Overview

FILL IN

---
''')