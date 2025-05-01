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
For the FOMC statements, we observed sentiment ratings ranging from strongly bearish (-0.7) to mildly bullish (0.2), with a trend toward neutral-slightly bullish from more recent statements. The statements also showed a mean sentiment score of approximately -0.1, indicating a slightly overall bearish inclination. The standard deviation for statements came in at 0.3, which was higher than the intermeeting minutes at 0.2, indicating that the statements contain more sentiment signals. 

For the intermeeting minutes, there were 11 documents that were unable to be processed, but with the vast majority we observed sentiment ratings ranging from moderately bearish (-0.5) to mildly bullish (0.2). The minutes had a slightly more positive mean for ratings at around neutral (0.0), showcasing less volatility than the statements. 

We created a more comprehensive dataset for correlation analysis by merging the sentiment scores with the market returns data, showcasing the strongest market reactions occurring on the day of announcements (T+0) and the following day (T+1), with diminishing effects afterward. Sector-wise, financial stocks (XLF) showed the strongest correlation with sentiment shifts, particularly for forward guidance sentiment, while utilities (XLU) showed the weakest correlation. When comparing document types, the statement sentiment showed stronger immediate market correlations, whilst the minute sentiment showed more prolonged effects over the following days. Throughout our analysis, the GPT-4 model demonstrated consistency in sentiment rating assignments across different document types and time periods

### Conclusions
Conclusions
The differences between the formal statements and the intermeeting minutes proved significant, with the statements showing a more pronounced sentiment relationship. The numerical rating approach aided greatly in these findings by providing a scalable method for tracking these communications over a substantial period of time. It was also demonstrated that large language models (GPT-4) can prove effective in analyzing sentiment in financial communications. 

These findings can extend to greater market predictions. An example of such being through serving as inputs for quant trading through their predictive value for short-term market movements. It could also prove fruitful as an additional indicator in monitoring economic conditions. From a financial institution perspective, this sentiment analysis could be useful in anticipating policy shifts to adjust risk profiles accordingly.

---
''')