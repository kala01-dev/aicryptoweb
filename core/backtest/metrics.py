import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    if len(returns) == 0 or returns.std() == 0:
        return 0
    return np.sqrt(252) * (returns.mean() - risk_free_rate) / returns.std()

def calculate_max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()
