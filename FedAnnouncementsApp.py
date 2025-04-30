import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title='FED Sentiment Dashboard',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ------------------ SIDEBAR NAV ------------------
with st.sidebar:
    st.markdown('## Navigation')
    st.markdown('Use the sidebar above to switch between sections of the dashboard.')
    st.markdown('[Fed Announcements Project Repo](https://github.com/jonahnathan0/Fed_Announcements)')

# ------------------ OVERVIEW ------------------
st.title('📈 Market Reactions to FED Announcements')

# Display image at the top
st.image('assets/Banking-December-FOMC-announcement-live-blog.jpg', use_container_width=True)

st.markdown('''
## Project Context

FILL IN

## Introduction

FILL IN

## Overview

FILL IN

---
''')