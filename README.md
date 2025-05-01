# Market Reactions to FED Announcements
By: Brian F, Jonah N, Kyle H, Haley J

[Streamlit Dasboard](https://fed-announcements.streamlit.app/)

[Instructions for this Project](https://ledatascifi.github.io/ledatascifi-2023/content/assignments/project.html)

### How to navigate the repo 
- Dataset_Build.ipynb
    - This is our main code where we created our final dataset
    - We pull stock returns here and perform the sentiment analysis
    - The ChatGPT analysis is merged into the final dataset here as well
- Scraping.ipynb
    - This is the code we used to scrape the FED announcment and FOMC intermeeting minutes
- ChatGPT_Sentiment
    - This is the code where we create our ChatGPT prompt to rank the statements from bullish to bearishness
    - Do not run this code because you will get an error (we removed the secret key for the API upon upload to the repo)
- Testing.ipynb
    - Ignore this file as well, this is where we were testing the ChatGPT API
- raw_data
    - Contains the HTML files for all of the annoucements
    - Contains the HTML files for all of the intermeeting minutes
    - Contains the final dataset
  


### Purpose
This project investigates how financial markets respond to Federal Reserve communications through a sentiment analysis of FOMC announcements. Using OpenAI API with GPT-4, we analyzed FOMC statements and meeting minutes to quantify shifts numerically. 


### Data 
Our dataset scraped FOMC announcements and intermeeting minutes from the Federal Reserve’s website from 2000 to 2024. These files were stored as “monetaryYYYYMMDD.html” and “fomcminutesYYYYMMDD.html”. In total, approximately 200 FOMC statements and number of meeting minutes were included in the dataset. 
For the market data, we collected the daily returns for each announcement, both 10 days prior and after. The data pulled from ten different indices.
The main U.S. indices include: S&P 500, NASDAQ, Dow Jones, Russell 2000, and Wilshire 5000. The sector-specific indices include: XLF, XLRE, XLU, XLY, XLP, XLE, XLV, XLI, XLB, XLK, and XLC. The treasury yields include the 3-month treasury bill and the 10-year treasury bill.


### Imported Libraries
```python

import os
import re
import glob
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import fnmatch
from time import sleep
from zipfile import ZipFile
from tqdm import tqdm
from utils.near_regex import *
import importlib
import openai
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events
```
