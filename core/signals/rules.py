def check_stop_loss_take_profit(entry_price, current_price, stop_loss_pct=0.02, take_profit_pct=0.05):
    if current_price <= entry_price * (1 - stop_loss_pct):
        return 'STOP_LOSS'
    elif current_price >= entry_price * (1 + take_profit_pct):
        return 'TAKE_PROFIT'
    return None
