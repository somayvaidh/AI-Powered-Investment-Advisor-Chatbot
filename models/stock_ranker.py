import pandas as pd
import yfinance as yf
import time

def get_nifty500_symbols():
    df = pd.read_csv("models/ind_nifty500list.csv")
    return df['Symbol'].dropna().unique().tolist()

def get_stock_metrics(symbol):
    try:
        stock = yf.Ticker(f"{symbol}.NS")
        info = stock.info
        
        name = info.get("shortName", symbol)
        market_cap = info.get("marketCap", None)
        pe_ratio = info.get("trailingPE", None)
        cmp = info.get("currentPrice", None)
        high_52 = info.get("fiftyTwoWeekHigh", None)
        low_52 = info.get("fiftyTwoWeekLow", None)

        if cmp and high_52:
            pct_below_high = round((high_52 - cmp) / high_52 * 100, 2)
        else:
            pct_below_high = None

        return {
            "name": name,
            "symbol": symbol,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "cmp": cmp,
            "52w_high": high_52,
            "52w_low": low_52,
            "%_below_high": pct_below_high
        }

    except Exception as e:
        print(f"❌ Failed to fetch {symbol}: {e}")
        return None

def get_top_stocks_raw(max_symbols=20):
    symbols = get_nifty500_symbols()
    results = []

    for symbol in symbols[:max_symbols]:
        try:
            stock = yf.Ticker(f"{symbol}.NS")
            info = stock.info
            name = info.get("shortName", symbol)
            market_cap = info.get("marketCap")
            pe_ratio = info.get("trailingPE", None)
            cmp = info.get("currentPrice", None)
            high_52w = info.get("fiftyTwoWeekHigh", None)
            low_52w = info.get("fiftyTwoWeekLow", None)

            if market_cap:
                results.append({
                    "symbol": symbol,
                    "name": name,
                    "market_cap": market_cap,
                    "pe_ratio": pe_ratio,
                    "cmp": cmp,
                    "52w_high": high_52w,
                    "52w_low": low_52w
                })
            else:
                print(f"Skipping {symbol}: no market cap")
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        
        time.sleep(1)

    return results


def get_top_stocks(n=5, max_symbols=20):
    raw_data = get_top_stocks_raw(max_symbols)
    top = sorted(raw_data, key=lambda x: x["market_cap"], reverse=True)[:n]
    return [f"{stock['name']} (Market Cap ₹{stock['market_cap']:,.2f}, P/E: {stock['pe_ratio']}, Current Price: ₹{stock['cmp']:,.2f})" for stock in top]


if __name__ == "__main__":
    top_stocks = get_top_stocks(n=5, max_symbols=20)
    print("\n🏆 Top 5 Stocks by Market Cap (with trader metrics):")
    top_stocks_raw = get_top_stocks_raw(20)
    print()
    for stock in top_stocks:
        print(stock)