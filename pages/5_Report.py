import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title='Market Returns', layout='wide')
st.title('Report: Market Reactions to Central Bank Communications')

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
    </style>
""", unsafe_allow_html=True)

st.markdown('''
### Initial Hypothesis

We hypothesized that FOMC announcements would contain detectable sentiment patterns that could be categorized as Bearish, Neutral, or Bullish. From this, we predicted that bullish sentiments would be associated with higher short-term returns. We also anticipated that sentiment would often shift within a single announcement from beginning to end. Additionally, due to press conferences being unscripted, we believed there to be a stronger sentiment-return correlation than from formal statements/minutes. Lastly, we expected topic-specific sentiment to outperform the overall sentiment in explaining market returns. 

### Data

Our dataset scraped FOMC announcements and intermeeting minutes from the Fed’s website during the time period of 2000-2024. These files were stored as “monetaryYYYYMMDD.html” and “fomcminutesYYYYMMDD.html,” respectively. In total, approximately 200 FOMC statements and number of meeting minutes from the two decades were included in the dataset. 

For the market data, we gathered the daily returns (10 days before and after) for each announcement. The data pulled from 18 different indices. The main U.S. indices include: the S&P 500, NASDAQ, Dow Jones, Russell 2000, and Wilshire 5000. Sector-specific indices include: XLF, XLRE, XLU, XLY, XLP, XLE, XLV, XLI, XLB, XLK, and the XLC. The Treasury yields include: the 3-month Treasury Bill and 10-year Treasury.   

### Methodology
To start, we used a data processing pipeline to: load HTML files, extract announcement dates, parse HTML to extract clean text from the announcements using BeautifulSoup, and limit the text length to make sure the data was compatible with the API. We also used the traditional lexicon analysis approach that included both BHR sentiment and LM sentiment.

Our GPT-4 prompts asked for sentiment analysis for each announcement (from beginning to end), and a sentiment rating from -1 (Bearish) to 1 (Bullish). The model’s responses were then parsed by using regular expressions for numerical sentiment extraction. Exception handling was implemented in the case of documents failing to process correctly. We then organized the results into structured datasets by: adding meeting IDs, labeling the document types, and saving the data in CSV format to aid in future visualization analysis.  

### Data Analysis
For the FOMC statements, we observed sentiment ratings ranging from strongly bearish (-0.7) to mildly bullish (0.2), with a trend toward neutral-slightly bullish from more recent statements. The statements also showed a mean sentiment score of approximately -0.1, indicating a slightly overall bearish inclination. For the intermeeting minutes, there were 11 documents that were unable to be processed, but with the vast majority we observed sentiment ratings ranging from moderately bearish (-0.5) to mildly bullish (0.2). The minutes had a slightly more positive mean for ratings at around neutral (0.0), showcasing less volatility than the statements. 

When comparing all of the sentiment scores as well as the topic specific sentiment scores all in a correlation matrix, the data seems hectic. One thing to notice when looking at the correlation matrix is that on the days leading up to the announcement (T-10 - T-0), there is a stronger correlation and presence of more positive sentiment scores and positive returns. This is represented by the red boxes in the heatmap. Then after the announcement (T-0 - T-10), there is a weaker correlation between the two variables which represents slightly more negative correlations and weaker returns. This is represented by the blue boxes in the heatmap.
''')

st.image('assets/img2.png', use_column_width=True)

st.markdown('''
In turn, this causes there to be an overall decline in average return from a few days before the statements right up until a few days after. However, we do see the markets bounce back after the decline, as the days after moves closer to T-10. 
''')

st.image('assets/img.png', use_column_width=True)

st.markdown('''
Throughout our analysis, the GPT-4 model demonstrated consistency in sentiment rating assignments across different document types and time periods. When looking at the average return curve by sentiment bins that were decided using the ChatGPT implementation, there are a few conclusions to be drawn. The first is that the bin representing the bearish sentiment is significantly more volatile than the neutral and bullish bins after the announcement (T-0). One reason for this volatility in the bearish sentiment bin could be that negative market sentiment could reflect more uncertainty or fear from investors, which can lead to overreactions and more dramatic price adjustments in the markets. Additionally, bearish communications from the FED could imply that there is upcoming or unexpected tightening or a poor economic outlook, which can contribute to these price changes.

### Conclusions
Conclusions
There are a lot of potential conclusions that can be drawn from this analysis including general assumptions from seeing how the market reacts to FED announcements. In the time comparison page of the dashboard, users can look at an individual announcement and see how a stock index reacted to that announcement. For people who focus on specific indices, being able to see and compare how they react versus other indices on the same date is interesting.

---
''')