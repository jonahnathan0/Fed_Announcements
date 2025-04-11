# Project Proposal - FED Announcements
### Brian F, Jonah N, Kyle H, Haley J


## Research Question 
The purpose of this research project is to analyze the FED announcements that occur eight times a year and see how the market reacts.  Every FED announcement is at 2:00 pm EST with the posting of a two to three page document that sums up the FED decision. At 2:30 EST there is then a press conference with the FED chair and a transcript released for that via the FED website. Three weeks later, there is a transcript of the FED intermeeting minutes as well; we will be looking at all three of these pieces of information and performing a sentiment analysis on the documents. 

We will also be analyzing the sentiment of the following few topics - monetary policy decisions, economic conditions,  forward guidance, and balance sheet policy. Instead of only looking at the effect of the topics on the S & P 500,  we are also going to look at the effect of the topics on multiple indices, to hopefully find a trend between the FED announcement and specific markets. 

In The Financial Market Effect of FOMC Minutes, a 2013 study done by Carlo Rosa (1), examines the intraday effect of the FOMC statement and the FOMC minutes on asset prices. The study concludes that the release of the FOMC statement has a strong short term effect on asset prices and the FOMC minutes also has a relatively strong short term effect on asset prices.

The broader question we are addressing is how efficiently financial markets process and react to central bank communications, which has significant implications for the effectiveness of monetary policy transmission and market efficiency theory. Instead of focusing on the intraday effect, we are looking to analyze the effect of the FED announcements on a daily basis. The two questions we are trying to answer are - 
- How do the FOMC statement, the FOMC meeting transcript, and the FOMC minutes affect various markets on the days of the release and up to 10 days after the release? 
    - We hypothesize that the FOMC statement and FOMC meeting transcript will have a more volatile effect on the market than the FOMC minutes.
- How does more positive/negative sentiment overall correlate with the markets after the announcements, and how does positive/negative sentiment from our four topics correlate with the markets after the announcements? 

To evaluate our findings, we will use multiple metrics of success:
- R2 values from regression analyses of sentiment scores against market returns
- Statistical significance of correlations between sentiment indicators and market movements
- Comparison of predictive power across different doc types and different markets


## Necessary Data 
We are going to be using Yahoo Finance to get the data for the indices, which has data all the way back to 1998. We will be analyzing the FED announcements that we will collect directly from the Federal Reserve's official website (federalreserve.gov) starting from 2000 and going to 2024, all with HTML and PDF formats. We will use web scraping techniques (BeautifulSoup and Requests libraries) to download all relevant documents within our sample period. That means with 8 announcements each year, there should be 192 total announcements that will be analyzed, which will correlate to 192 rows. Since we will be looking at three different documents (FED statement, FOMC meeting transcript, and FOMC minutes), there will be 3 final datasets each with 192 rows. One issue is that the FED statement and FOMC meeting transcript occur on the same day, so we might combine those two documents and get the total sentiments of the new combined document. This way we will actually have 2 final datasets with 192 rows, instead of 3 final datasets with 192 rows. 

Some other potential issues we assume: different FED communication styles over 24 years, difficulty isolating market reactions to FED announcements from other news, potential delays accessing recent transcripts, and document formats being inconsistent across time.

The final dataset for each will have the following columns - 
- Date of announcement 
- Index 1, Index 2, Index 3, Index 4, etc.
- The following for each index: 
    - ret,  cumulative ret T to T2, cumulative ret T3 to T10
- Positive/Negative ML sentiment scores
- Positive/Negative LM sentiment scores 
- The following for each of the four topics:
    - Positive/Negative sentiment score


For our sentiment analysis methodology, we will use two approaches:
- Machine Learning (ML) approach using pre-trained models from the Hugging Face Transformers library, specifically FinBERT, which is trained on financial text
- Lexicon-based (LM) approach using the Loughran-McDonald financial sentiment dictionary, which is specifically designed for financial text analysis

For topic identification and sentiment analysis within topics, we are planning on using the Near_Regex function. Our data transformation process will involve extracting text from downloaded documents and cleaning it (removing headers, footnotes, and special characters). Next we will segment documents into the four topic areas using keyword identification and supervised classification. Next we will apply sentiment analysis techniques to each document and topic segment. Next, we will match sentiment scores with corresponding market returns for the appropriate time-frames. Finally, we will look to identify relationships between the sentiment and the different returns.

Our folder structure will be organized hierarchically with three main directories: raw_data (containing original FED documents and market data in separate subdirectories), processed_data (storing calculated sentiment scores and topic segmented docs), and analysis (with our outputs and visualizations).

Potential Inidices that we will be looking at - 

Major U.S Indices:
- S & P 500 
- NASDAQ Composite
- Dow Jones Industrial Average
- Russell 2000
- Wilshire 5000

U.S Sector Indices:
- Financials - XLF
- Real Estate - XLRE
- Utilitilites - XLY
- Consumer Discretionary XLY 
- Consumer Staples - XLP 
- Energy - XLE 
- Healthcare - XLV 
- Industrials - XLI 
- Materials - XLB 
- Information Technology - XLK 
- Communication Services - XLC 

Other Markets:
- Two-year treasury yield
- Ten-year treasury yield 
- Euro/U.S. dollar 
- Swiss franc/U.S. dollar 
- Japanese yen/ U.S. dollar

Sources:
1. https://www.newyorkfed.org/medialibrary/media/research/epr/2013/0913rosa.pdf 







