# AI-Powered-Investment-Advisor-Chatbot


This project is an AI-powered financial chatbot designed to assist users in making informed stock investment decisions. By combining sentiment analysis, market data aggregation, and natural language understanding, the chatbot delivers real-time insights into Indian stock market companies (focusing on the Nifty 500 index).

It acts as a personal stock analyst—automating the process of stock research, comparison, and analysis—based on user prompts.


Tech-Stack
Data Source	Yahoo Finance (via yfinance)
News Scraping	Google News via googlesearch using Beautifulsoup
Sentiment Model	HuggingFace DistilBERT Model
Backend	Python
Interface	Flask or CLI (extendable to Web/Chat)
Dataset	Nifty 500 Constituents (CSV)

# Future-Aspects-
 Portfolio Recommendations
Based on user preferences (risk, sectors, time horizon), suggest a personalized list of stocks.
Could include basic portfolio optimization techniques.
Will be analysing stocks and putting them in cluster format where similar stocks will be grouped
Will be passing through a algorithm of RL or DL to predict in future price also clubbing it with weights of News-sentiment so have a better accuracy
Need to pass through OPENAPI for better sentimental accuracy.


investment_chatbot/
├── app.py                      # Chat interface using Flask
├
│
├── agents/
│   ├── principal_agent.py      # Routes user queries to sub-agents
│   ├── market_analyst.py       # Analyzes news/sentiment
│   └── portfolio_planner.py    # Suggests allocations (optional for now) (To be done)
│
├── crawlers/
│   ├── news_crawler.py         # Scrapes recent market news
│   └──
│
├── vector_store/
│   ├── embedder.py             # Create embeddings for news/stocks
│   ├── faiss_index.py          # Semantic search (no DB)
│   └── vector_store_utils.py
│
├── models/
│   ├── stock_ranker.py         # Ranks stocks based on features
│   └── clusterer.py            # Clusters similar stocks (TO BE DONE/FUTURE ASPECTS
│
├── semantic_cache/             # JSON or Pickle-based in-memory cache
│   ├── news_cache.json         # Cached news sentiment 
│   └── stock_snapshot.json     # Cached stock data (e.g., daily crawl)
│
├── utils/
│   ├── nlp_utils.py            # Basic query parsing, intent detection
│   ├── logger.py
│   └── formatter.py            # Clean responses for user
│
└── frontend/
    └── templates/
        └── index.html          (TO BE DONE)

