import json
import os
import sys
from typing import List, Dict

import openai

# Set your OpenAI API Key
openai.api_key = ("OPENAI_API_KEY")  
# Add the root directory to sys.path to import from vector_store
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../vector_store")))
from faiss_index import NewsVectorSearch


class MarketAnalyst:
    def __init__(self):
        self.vector_search = NewsVectorSearch()
        self.vector_search.load_index()
        print("✅ Market Analyst initialized!")

    def query_news(self, user_query: str, top_k: int = 5) -> List[Dict]:
        print(f"🔍 Searching for news articles about: {user_query}")
        results = self.vector_search.query(user_query, top_k)
        print(f"🆔 Retrieved {len(results)} results.")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item.get('title', 'No Title')}")
        return results

    def analyze_sentiment_openai(self, text: str) -> Dict:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are a financial sentiment analysis model. Respond with 'Positive', 'Negative', or 'Neutral' sentiment only."},
                    {"role": "user", "content": f"Analyze the sentiment of the following news:\n\n{text}"}
                ],
                temperature=0
            )
            sentiment = response["choices"][0]["message"]["content"].strip()
            return {"label": sentiment, "score": 1.0}  # Dummy score
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return {"label": "Unknown", "score": 0.0}

    def analyze_sentiment(self, articles: List[Dict]) -> List[Dict]:
        sentiments = []
        for article in articles:
            title = article.get('title', 'Untitled')
            text = article.get('summary', title)  # fallback to title
            sentiment_result = self.analyze_sentiment_openai(text)
            sentiments.append({
                "title": title,
                "sentiment": sentiment_result['label'],
                "score": sentiment_result['score']
            })
        return sentiments

    def get_analytical_report(self, user_query: str, top_k: int = 5) -> List[Dict]:
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
