import pandas as pd
import numpy as np
import yfinance as yf

def main():
    # Get user inputs
    stock = input("Stock symbol: ").upper()
    start = input("Start date (YYYY-MM-DD): ")
    end = input("End date (YYYY-MM-DD): ")
    interval = input("Interval (1d/1wk/1mo): ")
    investment = int(input("Enter the amount invested (in INR): "))
    
    # Fetch data
    data = yf.Ticker(stock).history(start=start, end=end, interval=interval)
    
    # Save to CSV
    filename = f"{stock}_{start}_{end}.csv"
    data.to_csv(filename)
    print(f"✅ Data saved to {filename}")
    
    # Process data - keep only Close price
    df = pd.read_csv(filename, index_col=0)
    df = df[['Close']].copy()  # Keep only Close column
    print(df)

    # Get moving average periods
    short_ma_period = int(input("Enter the no. of days for first moving average: "))
    long_ma_period = int(input("Enter the no. of days for second moving average: "))
    
    # Calculate moving averages
    df[f'{short_ma_period} PMA'] = df['Close'].rolling(window=short_ma_period).mean()
    df[f'{long_ma_period} PMA'] = df['Close'].rolling(window=long_ma_period).mean()

    # Generate trading signals (vectorized approach)
    df['signal'] = (df[f'{short_ma_period} PMA'] > df[f'{long_ma_period} PMA']).astype(int)
    
    print(df)

    # Calculate returns
    buy_and_hold_return, strategy_return = calculate_returns(df, long_ma_period, investment)

    print(f'Normal Return: {buy_and_hold_return*100} %')
    print(f'Indicator Return: {strategy_return*100} %')
    # df.to_csv('C:/Users/Sahas/OneDrive/Desktop/Peeyush/Project.csv')


def calculate_returns(df, start_period, investment):
    """Calculate returns for buy-and-hold vs trading strategy"""
    start_index = start_period - 1
    total_days = len(df)
    
    # Initialize variables
    buy_and_hold_portfolio = 0
    strategy_portfolio = 0
    num_of_stocks = 0
    initial_investment = investment

    # Find first valid signal (after moving averages are calculated)
    valid_data = df.iloc[start_index:].dropna()
    if valid_data.empty:
        return 0, 0
    
    # Get first buy signal or initial position
    buy_index = start_index
    if valid_data.iloc[0]['signal'] == 1:
        # Initial buy
        buy_price = valid_data.iloc[0]['Close']
        num_of_stocks = investment / buy_price
        strategy_portfolio = 0
    else:
        # Find first buy signal
        signal_changes = valid_data['signal'].diff()
        first_buy = signal_changes[signal_changes > 0].index
        if len(first_buy) > 0:
            buy_index = df.index.get_loc(first_buy[0])
            buy_price = df.iloc[buy_index]['Close']
            num_of_stocks = investment / buy_price
            strategy_portfolio = 0

    # Execute trading strategy using signal changes
    signal_changes = df['signal'].diff()
    
    for idx in signal_changes.index:
        if pd.isna(signal_changes[idx]):
            continue
            
        if signal_changes[idx] == -1:  # Sell signal (1 to 0)
            strategy_portfolio = num_of_stocks * df.loc[idx, 'Close']
            num_of_stocks = 0
        elif signal_changes[idx] == 1:  # Buy signal (0 to 1)
            if strategy_portfolio > 0:
                num_of_stocks = strategy_portfolio / df.loc[idx, 'Close']
                strategy_portfolio = 0

    # Calculate final returns
    final_price = df.iloc[-1]['Close']
    buy_price = df.iloc[buy_index]['Close']
    
    # If still holding stocks, sell at final price
    if num_of_stocks > 0:
        strategy_portfolio = num_of_stocks * final_price
    
    # Calculate returns
    buy_and_hold_return = (final_price / buy_price) - 1
    strategy_return = (strategy_portfolio / initial_investment) - 1

    return buy_and_hold_return, strategy_return


if __name__ == "__main__":
    main()