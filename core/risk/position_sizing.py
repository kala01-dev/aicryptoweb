def calculate_position_size(balance, entry_price, stop_loss_price, risk_pct=0.02, max_position_pct=0.2):
    risk_amount = balance * risk_pct
    stop_distance = abs(entry_price - stop_loss_price)
    if stop_distance == 0:
        return 0
    position_size = risk_amount / stop_distance
    max_position_value = balance * max_position_pct
    max_position_size = max_position_value / entry_price
    return min(position_size, max_position_size)
