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
As mentioned above, the first step was to load in the index tickers.
''')

st.image('assets/img3.png', use_container_width=True)

st.markdown('''
Next, we loaded a dataset that included the dates of every FED statement announcement. There was no dataset online of the date of every intermeeting minutes online, so we had to manually input those dates in a corresponding column. 

Next, we loaded the return data for all of the tickers on the date of the statements, as well as classified the announcement type as a statement. This got us an original dataset that looks like the following:
''')

st.image('assets/img4.png', use_container_width=True)

st.markdown('''There were lots of <NA> values scattered throughout the dataset, which were caused due to those days being non-trading days. Most of the <NA> values came in sets of two, which represented the weekends, and Yahoo Finance ignored these days. To fix this problem we actually expanded the search window to around 15 days on either side of the announcement date, and pulled the first 10 valid values on each side

We then followed this exact same procedure for the intermeeting announcements, which got us a dataset that looked like the following:
''')

st.image('assets/img5.png', use_container_width=True)

st.markdown('''
A meeting ID was assigned to every statement and intermeeting announcement. There were 200 statements with meeting ID’s from 1-200 and 200 corresponding intermeeting minutes with meeting ID’s from 1-200. For example, statement number 5 would match to the corresponding intermeeting number 5. This was necessary because the intermeeting minutes are released many weeks after the matching statement, and sometimes there was another statement release before the intermeeting minutes were released. 

For the sentiment analysis, we loaded the BHR and LM (Loughran-McDonald) sentiment dictionaries. We then compiled the regex for all both dictionaries, and for the positive and negative output for both with the following code:
''')

st.image('assets/img6.png', use_container_width=True)

st.markdown('''
Next, we used a function to compute the sentiment scores of all of the processed html files of the statements and intermeeting notes. This function loops through the files, reads and parses the html file, extracts and cleans the text, computes normalized sentiment scores, and then stores the results:
''')

st.image('assets/img7.png', use_container_width=True)

st.markdown('''
Next we implemented the contextual sentiment analysis on the documents by looking at four topics - monetary policy, economic policy, future outlook, and balance sheet. Each bit of code for the topics are similar, the only difference is the word lists. The code goes by the following steps:
- 1 - Define keywords 
- 2 - Define source folders with the HTML files 
- 3 - Loops for going through files and going over document type
''')

st.image('assets/img8.png', use_container_width=True)

st.markdown('''
- 4 - Read and Preprocess HTML Text
''')

st.image('assets/img9.png', use_container_width=True)

st.markdown('''
- 5 - Count positive/negative sentiment near keywords using the NEAR_finder() function
''')

st.image('assets/img10.png', use_container_width=True)

st.markdown('''
- 6 - Normalize and store results
''')

st.image('assets/img11.png', use_container_width=True)

st.markdown('''We then performed the ChatGPT analysis that consisted of the following steps:
- 1 - Pip install OpenAI 
- 2 - Import OpenAI and input the secret API key
''')

st.image('assets/img12.png', use_container_width=True)

st.markdown('''
- 3 - Looped over dated files
''')

st.image('assets/img13.png', use_container_width=True)

st.markdown('''
- 4 - Open and parse the HTML file 
''')

st.image('assets/img14.png', use_container_width=True)

st.markdown('''
- 5 - Construct prompt
''')

st.image('assets/img15.png', use_container_width=True)

st.markdown('''
- 6 - Send prompt to GPT-4
''')

st.image('assets/img16.png', use_container_width=True)

st.markdown('''
- 7 - Extract numerical rating and convert to a float 
''')

st.image('assets/img17.png', use_container_width=True)

st.markdown('''
This GPT process outputted a sentiment rating from -1 (bearish) to 1 (bullish), for meeting ID’s 1-200 for both the statements and the intermeeting minutes. Next we merged all of the GPT analysis into the final dataset using the following code
''')

st.image('assets/img18.png', use_container_width=True)

st.markdown('''
### Data Analysis
For the FOMC statements, we observed sentiment ratings ranging from strongly bearish (-0.7) to mildly bullish (0.2), with a trend toward neutral-slightly bullish from more recent statements. The statements also showed a mean sentiment score of approximately -0.1, indicating a slightly overall bearish inclination. For the intermeeting minutes, there were 11 documents that were unable to be processed, but with the vast majority we observed sentiment ratings ranging from moderately bearish (-0.5) to mildly bullish (0.2). The minutes had a slightly more positive mean for ratings at around neutral (0.0), showcasing less volatility than the statements. 

When comparing all of the sentiment scores as well as the topic specific sentiment scores all in a correlation matrix, the data seems hectic. One thing to notice when looking at the correlation matrix is that on the days leading up to the announcement (T-10 - T-0), there is a stronger correlation and presence of more positive sentiment scores and positive returns. This is represented by the red boxes in the heatmap. Then after the announcement (T-0 - T-10), there is a weaker correlation between the two variables which represents slightly more negative correlations and weaker returns. This is represented by the blue boxes in the heatmap.
''')

st.image('assets/img2.png', use_container_width=True)

st.markdown('''
In turn, this causes there to be an overall decline in average return from a few days before the statements right up until a few days after. However, we do see the markets bounce back after the decline, as the days after moves closer to T-10. 
''')

st.image('assets/img.png', use_container_width=True)

st.markdown('''
Throughout our analysis, the GPT-4 model demonstrated consistency in sentiment rating assignments across different document types and time periods. When looking at the average return curve by sentiment bins that were decided using the ChatGPT implementation, there are a few conclusions to be drawn. The first is that the bin representing the bearish sentiment is significantly more volatile than the neutral and bullish bins after the announcement (T-0). One reason for this volatility in the bearish sentiment bin could be that negative market sentiment could reflect more uncertainty or fear from investors, which can lead to overreactions and more dramatic price adjustments in the markets. Additionally, bearish communications from the FED could imply that there is upcoming or unexpected tightening or a poor economic outlook, which can contribute to these price changes.

### Conclusions
There are a lot of potential conclusions that can be drawn from this analysis including general assumptions from seeing how the market reacts to FED announcements. In the time comparison page of the dashboard, users can look at an individual announcement and see how a stock index reacted to that announcement. For people who focus on specific indices, being able to see and compare how they react versus other indices on the same date is interesting.

---
''')