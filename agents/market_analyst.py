import json
import numpy as np
from transformers import pipeline,AutoTokenizer, AutoModelForSequenceClassification
import sys
import os

# Add the root directory to the sys.path so Python can find 'vector_store'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "c:/chatbot financial/vector_store")))
from faiss_index import NewsVectorSearch

sentiment_analyzer = pipeline("sentiment-analysis")
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


class MarketAnalyst:
    def __init__(self):
        self.vector_search = NewsVectorSearch()
        self.vector_search.load_index()
        print("✅ Market Analyst initialized!")

    def query_news(self, user_query, top_k=5):
        print(f"🔍 Searching for news articles about: {user_query}")
        results = self.vector_search.query(user_query, top_k)
    
        print(f"🆔 Retrieved {len(results)} results.")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item.get('title', 'No Title')}")

        return results


    def analyze_sentiment(self, articles):
        sentiments = []
        for article in articles:
            title = article.get('title', 'Untitled')
            text = article.get('summary', title)  # fallback to title
            sentiment_result = sentiment_analyzer(text)[0]
            sentiments.append({
                "title": title,
                "sentiment": sentiment_result['label'],
                "score": sentiment_result['score']
            })
        return sentiments

    def get_analytical_report(self, user_query, top_k=5):
        news_results = self.query_news(user_query, top_k)
        if not news_results:
            return []

        sentiment_results = self.analyze_sentiment(news_results)

        report = []
        for sentiment in sentiment_results:
            report.append({
                "Title": sentiment["title"],
                "Sentiment": sentiment["sentiment"],
                "Confidence Score": sentiment["score"]
            })

        return report

if __name__ == "__main__":
    analyst = MarketAnalyst()
    user_query = "360 ONE WAM Ltd performance"

    report = analyst.get_analytical_report(user_query, top_k=5)

    print("\n📈 Sentiment Analysis Report:")
    if not report:
        print("No articles to display.")
    else:
        for i, item in enumerate(report, 1):
            print(f"{i}. {item['Title']}")
            print(f"   Sentiment: {item['Sentiment']} (Confidence: {item['Confidence Score']:.2f})\n")
