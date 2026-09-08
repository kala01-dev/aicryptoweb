"""Indikator sentimen makro pasar."""
def get_fear_greed_index():
    try:
        import requests
        resp = requests.get('https://api.alternative.me/fng/', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return int(data['data'][0]['value'])  # 0-100
    except:
        pass
    return 50  # netral

def get_macro_sentiment_score():
    fng = get_fear_greed_index()
    return fng
