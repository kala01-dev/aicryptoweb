def get_stop_loss_take_profit(entry_price, atr_value, side='buy', sl_mult=2.0, rr_ratio=2.0):
    if side == 'buy':
        stop_loss = entry_price - sl_mult * atr_value
        take_profit = entry_price + sl_mult * rr_ratio * atr_value
    else:
        stop_loss = entry_price + sl_mult * atr_value
        take_profit = entry_price - sl_mult * rr_ratio * atr_value
    return stop_loss, take_profit
