def combine_scores(tech_score, fund_score, news_score, ml_prob, weights=(0.5,0.3,0.2)):
    base_score = weights[0]*tech_score + weights[1]*fund_score + weights[2]*news_score
    total = base_score * 0.7 + (ml_prob * 100) * 0.3
    return total
