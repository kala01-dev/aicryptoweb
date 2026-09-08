import requests
import xml.etree.ElementTree as ET
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

analyzer = SentimentIntensityAnalyzer()

RSS_FEEDS = [
    'https://cointelegraph.com/rss',
    'https://coindesk.com/arc/outboundfeeds/rss/',
    'https://decrypt.co/feed',
    'https://www.theblock.co/rss.xml',
]

_news_cache = {'timestamp': None, 'articles': []}

def fetch_news(limit=15):
    global _news_cache
    if _news_cache['timestamp'] and (datetime.now() - _news_cache['timestamp']).seconds < 1800:
        return _news_cache['articles']
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            resp = requests.get(feed_url, timeout=5)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                items = root.findall('.//item')[:limit]
                for item in items:
                    title = item.find('title').text if item.find('title') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    source = feed_url.split('/')[2].replace('www.', '')
                    articles.append({'title': title, 'link': link, 'published': pub, 'source': source})
        except:
            continue
    _news_cache['timestamp'] = datetime.now()
    _news_cache['articles'] = articles
    return articles

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)['compound']

def get_news_sentiment_score(symbol):
    news = fetch_news(limit=10)
    if not news:
        return 50, []
    symbol_clean = symbol.replace('USDT', '').lower()
    relevant = [n for n in news if symbol_clean in n['title'].lower()]
    if not relevant:
        relevant = news[:3]
    sentiments = [analyze_sentiment(n['title']) for n in relevant]
    avg = sum(sentiments) / len(sentiments) if sentiments else 0
    score = 50 + avg * 50
    return min(100, max(0, score)), relevant
