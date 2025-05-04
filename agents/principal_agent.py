from market_analyst import MarketAnalyst
from stock_ranker import get_top_stocks, get_stock_metrics
from stock_ranker import get_top_stocks_raw

class PrincipalAgent:
    def __init__(self):
        self.market_analyst = MarketAnalyst()

    def route_query(self, user_query):
        query_lower = user_query.lower()

        if any(keyword in query_lower for keyword in ["news", "sentiment", "performance", "report"]):
            return self.handle_market_analysis(user_query)

        elif any(keyword in query_lower for keyword in ["stock", "invest"]):
            return self.handle_stock_ranking()

        elif "combine" in query_lower:
            return self.handle_combined_report(user_query)

        else:
            return f"🤖 Sorry, I couldn't understand your request: '{user_query}'. Try asking about stock news or investments."

    def handle_market_analysis(self, user_query):
        company_name = self.extract_company_name(user_query)
        report = self.market_analyst.get_analytical_report(user_query)
        
        # Fetch company details
        company_info = get_stock_metrics(company_name)

        if not report:
            sentiment_report_text = "📉 No relevant news articles found for that query."
        else:
            sentiment_report_text = "\n📊 Market Sentiment Report:\n"
            for i, item in enumerate(report, 1):
                sentiment_report_text += f"{i}. {item['Title']}\n"
                sentiment_report_text += f"   Sentiment: {item['Sentiment']} (Confidence: {item['Confidence Score']:.2f})\n"

        if company_info:
            company_info_text = f"\n📊 Company Details:\n"
            company_info_text += f"Name: {company_info['name']}\n"
            company_info_text += f"Symbol: {company_info['symbol']}\n"
            company_info_text += f"Market Cap: ₹{company_info['market_cap']:,.2f}\n"
            company_info_text += f"P/E Ratio: {company_info['pe_ratio']}\n"
            company_info_text += f"Current Price: ₹{company_info['cmp']:,.2f}\n"
            company_info_text += f"52-week High: ₹{company_info['52w_high']:,.2f}\n"
            company_info_text += f"52-week Low: ₹{company_info['52w_low']:,.2f}\n"
            company_info_text += f"Percentage Below 52-week High: {company_info['%_below_high']}%\n"
        else:
            company_info_text = "\n📊 Company details not found."

        combined_report = "\n📈 Combined Stock Ranking and Sentiment Analysis Report:\n"
        combined_report += company_info_text + "\n\n"
        combined_report += sentiment_report_text

        return combined_report

    def extract_company_name(self, user_query):
        """
        Extract company name (or symbol) from user query.
        """
        if "360 ONE WAM Ltd" in user_query:
            return "360 ONE WAM Ltd"
        # Add more logic for other companies if needed
        return user_query