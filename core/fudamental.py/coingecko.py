from core.data.fetcher import get_coin_market_data

def get_fundamental_score(coingecko_id):
    data = get_coin_market_data(coingecko_id)
    if not data:
        return 50
    market_data = data.get('market_data', {})
    score = 0
    rank = market_data.get('market_cap_rank')
    if rank:
        if rank <= 10:
            score += 30
        elif rank <= 50:
            score += 20
        else:
            score += 10
    else:
        score += 15

    volume = market_data.get('total_volume', {}).get('usd', 0)
    mcap = market_data.get('market_cap', {}).get('usd', 0)
    if mcap > 0:
        ratio = volume / mcap
        if ratio > 0.1:
            score += 20
        elif ratio > 0.05:
            score += 15
        else:
            score += 5
    else:
        score += 10

    change_7d = market_data.get('price_change_percentage_7d', 0)
    if change_7d is not None:
        if change_7d > 10:
            score += 20
        elif change_7d > 0:
            score += 15
        elif change_7d > -10:
            score += 10
        else:
            score += 5
    else:
        score += 10

    circulating = market_data.get('circulating_supply')
    max_supply = market_data.get('max_supply')
    if max_supply and circulating:
        ratio = circulating / max_supply
        if ratio < 0.5:
            score += 20
        else:
            score += 10
    else:
        score += 10

    return min(score, 100)
