import streamlit as st
from streamlit.components.v1 import html

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title='Overview (Home)',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ------------------ SIDEBAR NAV ------------------
with st.sidebar:
    st.markdown('## Navigation')
    st.markdown('Use the sidebar above to switch between sections of the dashboard.')

    st.markdown('[🔗 GitHub Repo](https://github.com/jonahnathan0/Fed_Announcements)')

# ------------------ OVERVIEW ------------------
st.title('📈 Market Reactions to FED Announcements')

st.markdown('''
## Project Context

Central bank communication has become one of the most closely watched events in financial markets. The release of Federal Reserve statements, press conferences, and meeting minutes can move markets significantly, not just based on actual rate decisions but on the **tone and sentiment** of the messaging.

Our project analyzes how financial markets respond to different types of Federal Reserve communications using **sentiment analysis models** (including ChatGPT) and visualizes **market return behavior** around these announcements.

We created a dashboard that allows users to explore:
- Market reactions to specific communication types (statement, intermeeting)
- Sentiment scores derived from NLP models
- Correlation heatmaps of returns and sentiment
- Time-based comparisons
- An executive report summarizing key findings

## Why This Project?

This project began from an interest in combining:
- Central bank transparency and its growing importance
- Financial market volatility around FOMC events
- Modern language models’ ability to evaluate sentiment

Rather than looking solely at interest rate changes or policy decisions, we wanted to ask:  
**“How much of market behavior can be attributed to the _wording_ and _tone_ of communication itself?”**

## Tools Used

- **Python & Streamlit** for dashboard development
- **Pandas, Seaborn, Matplotlib** for data wrangling and plotting
- **OpenAI GPT sentiment scoring** (experimental)
- **Multiple financial indices** and announcement types

## Quick Demo

Use the sidebar to navigate across different views:
1. **Market Returns**  
   Explore return patterns around T-10 to T+10 for FOMC events

2. **Time Comparison**  
   Compare market response across different time periods

3. **ChatGPT Sentiment**  
   View sentiment generated from LLM-based scoring (experimental)

4. **Report**  
   Executive-style summary of findings and recommendations

---
''')