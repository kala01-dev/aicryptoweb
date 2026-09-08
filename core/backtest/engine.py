from core.signals.engine import calculate_technical_score
from core.ml.predict import get_ml_probability

def backtest_signal(symbol, df, initial_balance=10000, fee_rate=0.001):
    balance = initial_balance
    position = 0
    entry_price = 0
    trades = []
    step = 5
    for i in range(50, len(df)-1, step):
        sub_df = df.iloc[:i+1].copy()
        tech_score, _ = calculate_technical_score(sub_df)
        ml_prob = get_ml_probability(symbol, sub_df)
        combined_score = tech_score * 0.7 + (ml_prob * 100) * 0.3
        current_price = sub_df['close'].iloc[-1]
        if combined_score >= 65 and position == 0:
            entry_price = current_price
            position = balance / entry_price
            balance = 0
            trades.append({'action': 'BUY', 'price': entry_price, 'time': sub_df.index[-1]})
        elif combined_score <= 35 and position > 0:
            exit_price = current_price
            balance = position * exit_price * (1 - fee_rate)
            trades.append({'action': 'SELL', 'price': exit_price, 'time': sub_df.index[-1]})
            position = 0
    if position > 0:
        exit_price = df['close'].iloc[-1]
        balance = position * exit_price * (1 - fee_rate)
        trades.append({'action': 'SELL', 'price': exit_price, 'time': df.index[-1]})
        position = 0
    roi = (balance - initial_balance) / initial_balance * 100
    wins = 0
    losses = 0
    for i in range(0, len(trades)-1, 2):
        if trades[i+1]['price'] > trades[i]['price']:
            wins += 1
        else:
            losses += 1
    win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
    return {
        'final_balance': balance,
        'roi': roi,
        'win_rate': win_rate,
        'num_trades': len(trades)//2,
        'trades': trades
    }
