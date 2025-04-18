# Project Proposal - FED Announcements
### Brian F, Jonah N, Kyle H, Haley J


## Research Question 
This project investigates how the financial markets respond to the Federal Reserve’s three primary modes of communication: the 2:00 PM FOMC Statement, the 2:30 PM Press Conference Transcript, and the FOMC meeting minutes. Prior work on this topic shows that financial markets have a strong response to FOMC communications, but this work is focused on intraday data (Carlo Rosa, 2013)(1). Instead we will be looking at daily return data from 10 days prior leading up to the FED announcement and 10 days after the announcement. 

The big picture question we are trying to answer is: How do financial markets process monetary policy information from central bank communications, and can sentiment extracted from these texts explain market movements? 

* The italicized text will be explained at the bottom

More specific research questions:
- Do textual sentiment and structured views derived from central bank communications significantly predict short-term market reactions?
- What type of FOMC communication has the most predictive power for financial market movements?
- Can topic-specific sentiment better explain market responses than general sentiment?
- Do LLM-based structured sentiment labels add explanatory value over standard NLP sentiment tools? 
- Can a temporally constrained language model like ChronoBERT enhance the realism and accuracy of our sentiment scoring by replicating investor information sets at the time of each communication?

This is a relationships-based project. Our hypotheses include:
- Bullish sentiment or views extracted from communications are associated with higher short-term returns 
- Topic-specific sentiment will outperform overall sentiment in explaining returns 
- Press conferences, being unscripted, will show stronger sentiment return correlations than statements or minutes 
- Structured sentiment from LLMs will add explanatory power over traditional NLP methods 
- ChronoBERT-generated sentiment will be more accurate than other methods by better replicating real-time investor perspectives without lookahead bias 


## Necessary Data 
We are going to be using Yahoo Finance to get the data for the indices, which has data all the way back to 1998. We will be analyzing the FED announcements that we will collect directly from the Federal Reserve's official website (federalreserve.gov) starting from 2000 and going to 2024, all with HTML and PDF formats. We will use web scraping techniques (BeautifulSoup and Requests libraries) to download all relevant documents within our sample period. That means with 8 announcements each year, there should be 192 total announcements that will be analyzed. Since we will be looking at three different documents (FED statement, FOMC meeting transcript, and FOMC minutes), there will be 3 final datasets each with 192 announcements each. One issue is that the FED statement and FOMC meeting transcript occur on the same day, so we will combine those two documents and get the total sentiments of the new combined document.

Some other potential issues we assume: potential delays accessing recent transcripts, one off announcements that are missing one of the three documents we are analyzing, and document formats being inconsistent across time.

We are going to be looking at the index returns every day from 10 days prior to the announcement to 10 days after the announcement. We will also be looking at many indices so the amount of rows/columns (depends if we do wide or long format) will multiply by 20 (for the days) and by the number of indices.
For example, the final dataset format should look like this (wide format):

| Category       | Variable(s)                                                               | Description                                                       |
|---------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|
| 1. Event Data| Event_id, Date, Doc_type, Doc_url                                          | Unique ID, Date of the event, Type of document (statement, press <br> conference, intermeeting minutes), URL to Source  |
| 2. Market Returns    | SP500_ret(-10) to SP500_ret(10), NASDAQ_ret(-10) to NASDAQ_ret (10), <br> DIJA_ret(-10) to DIJA_ret(10), Etc.    | The daily log of returns from 10 days before to 10 days after each FOMC communication for each index  |
| 3. Textual Sentiment Metrics     | Interactive dashboard for viewing analytics and managing settings.         | Includes charts, export tools, and user management options.      |
| 4. Topic Specific Sentiment| Supports login via email, Google, and SSO.                                 | Google requires OAuth setup.                                     |
| 5. LLM-Based Structured Labels    | REST API with rate limiting and API key support.                           | Rate limit is 1000 requests/hour.<br>More available on request.  |
| Dashboard     | Interactive dashboard for viewing analytics and managing settings.         | Includes charts, export tools, and user management options.      |

Our folder structure will be organized hierarchically with three main directories: raw_data (containing original FED documents and market data in separate subdirectories), processed_data (storing calculated sentiment scores and topic segmented docs), and analysis (with our outputs and visualizations).


## Ambition
We want to perform a similar analysis to the mid-term project but go beyond that and see what is possible with NLP applications for finance. Our project has the following aspects - 
- Sentiment analysis: Combining analysis for an LM dictionary, ML dictionary, and LLM views 
- Topic specific focus: Each FED communication will be looked at for sentiment by specific topics
- Multi-document framework: Analyze two separate narratives. The first being the combination of the FED statement and the FED meeting minutes which occur on the same day. The second being the analysis of the FOMC intermeeting minutes which are released three weeks after the statement/meeting transcript.
- Dynamic dashboard: Provide a shareable, and interactive website for users to explore the project. 

Everything above that is italicized represents an advanced extension that we will be attempting to look at called ChronoBERT. This is a temporally aware LLM model that is trained on data from financial texts prior to the event that is being analyzed (announcement date). This avoids forward looking bias and may potentially outperform the normal models we use. This method “freezes” the model’s information at T-1, which helps allow us to mimic investor sentiment that could realistically be inferred at the time. 

This project merges classic NLP, sentiment analysis, LLM reasoning, and temporal AI, to try and understand the central bank influence on financial markets.


Sources:
1. https://www.newyorkfed.org/medialibrary/media/research/epr/2013/0913rosa.pdf 







