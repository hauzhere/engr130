"""
===============================================================================
ENGR 13000 Spring 2025

Program Description
    This program analyzes, compares and visualizes the performance of two bipartisan ETFs, NANC and KRUZ, against the S&P 500 index. 
    It performs event studies to manually and automatically using Congress.gov API to identify significant events that impact the performance of these ETFs.
Assignment Information
    Assignment:     Ind Project 4
    Author:         Layla Le, le306@purdue.edu
    Team ID:        001 - 12 

Contributor:    Yi Ding (ECE 20875 instructor), yiding@purdue.edu
    My contributor(s) helped me:
    [X] understand the assignment expectations without
        telling me how they will approach it.
    [X] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
Contributor:    Lulu Zeng (MGMT 41310 instructor), zeng135@purdue.edu
    My contributor(s) helped me:
    [X] understand the assignment expectations without
        telling me how they will approach it.

    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""


# Write any import statements here (and delete this comment).
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
from datetime import datetime, timedelta
import requests #processing API requests



#---------------------------------------------------
#  Inputs
#HARD-CODED TICKERS FOR SAMPLE PORTFOLIO INPUT
def get_tickers(): 
    return ['NANC', 'KRUZ', '^GSPC', 'QQQM', 'XOM', 
            'LMT', 'TEMP', 'AAPL', 'MSFT', 'AMZN', 
            'GOOGL', 'META', 'NVDA', 'TSLA', 'BRK-B', 
            'JPM', 'V', 'UNH', 'PG', 'HD', 'MA', 
            'DIS', 'XLV', 'VDE']

# ASSIGN INCEPTION DATES FOR SAMPLE PORTFOLIO 
def get_inception_dates():
    tickers = get_tickers()
    return {tkr: '2023-02-07' for tkr in tickers} 

#UPDATE TODAY'S DATE
def get_today():
    return datetime.today().strftime('%Y-%m-%d')

# USER INPUTS EVENT DATE FOR MANUAL EVENT STUDY
def choose_date():
    date = input("Enter event date (YYYY-MM-DD): ")
    try:
        return pd.to_datetime(date).strftime('%Y-%m-%d') #Convert string to datetime
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return choose_date() #recurring function to ask for date again
    
# PORTFOLIO DATA INPUT
def input_data():
    try:
        data = yf.download(
            list(get_tickers()), #call function
            start=get_inception_dates()['NANC'], #Start date from inception date",
            end=get_today(),
            auto_adjust=False
        )['Close'] #Retrieve closing prices of tickers from Yahoo Finance
        data.attrs['inception_dates'] = get_inception_dates() 
        # Here, I had to store a dictionary of ticker with their corresponding inception dates in attrs attribute of data because pandas does not allow adding attributes to data frame
        return data
    except Exception as e: #Error checking
        print(f"Data fetch failed: {e}")
        return None    
    
#---------------------------------------------------


#---------------------------------------------------
#  Computations
# DATA CLEANING 
def clean_data(data):
    cleaned = data.copy() # Create a copy to clean to avoid changing original data
    
    # Access inception_date dictionary from attrs
    inception_dates = data.attrs.get('inception_dates', {})
    
    for tkr, start in inception_dates.items():
        start_dt = pd.to_datetime(start) # Convert string to datetime
        cleaned.loc[cleaned.index < start_dt, tkr] = np.nan  # Ignore data before inception dates
    
    cleaned = cleaned.ffill().dropna(how='all')  # Forward fill missing values and drop rows with all NaNs
    
    # Reassign inception_dates back to attrs
    cleaned.attrs['inception_dates'] = inception_dates
    
    return cleaned
    

# EVENT STUDY 
def run_event_study(data, ticker, event_date,
                    event_window=(-5, 10), estimation_window=(-120, -21), 
                    market_col='^GSPC'):
    #market_col = '^GSPC' #S&P 500 as market index
    event_date = pd.to_datetime(event_date) #Convert string to datetime
    returns = data[[ticker, market_col]].pct_change().dropna() 
    #Calculate daily returns of the market index and other ticker columns in the portfolio data frame by computing market changes in percentage and skip empty rows
    
    if event_date not in returns.index: 
        raise ValueError(f"Event date not in record") #Error checking

    # Estimation window to calculate the normal relationship between stick and market returns
    loc = returns.index.get_loc(event_date) #Use pandas get_loc to find the position of the event date in data frame
    est_start = loc + estimation_window[0] #Estimation window start
    est_end = loc + estimation_window[1] #Estimation window end
    
    # Process data in the estimation window
    estimation_returns = returns.iloc[est_start:est_end].dropna() #Drop empty rows in the estimation window
    r_stock = estimation_returns[ticker] #Daily returns of the ticker in the estimation window
    r_market = estimation_returns[market_col] #Daily returns of the market index in the estimation window

    # Linear regression model
    model = LinearRegression().fit(r_market.values.reshape(-1, 1), r_stock.values) 
    alpha, beta = model.intercept_, model.coef_[0]

    # Event window
    evt_start = loc + event_window[0]
    evt_end = loc + event_window[1]
    event_returns = returns.iloc[evt_start:evt_end + 1].dropna() #last event is inclusive
    r_evt_stock = event_returns[ticker].values
    r_evt_market = event_returns[market_col].values

#FINANCIAL METRICS IN CAPITAL ASSET PRICING MODEL, MGMT 41310
    expected = alpha + beta * r_evt_market
    abnormal = r_evt_stock - expected

    car = abnormal.sum()
    resid = r_stock.values - (alpha + beta * r_market.values)
    stderr = np.std(resid, ddof=1)
    se_car = stderr * np.sqrt(len(abnormal))
    t_stat = car / se_car
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(r_stock)-2)) #ECE 20875

    return car, t_stat, p_value


# STATISTICAL METRICS TO COMPARE BIPARTISAN ETFs VS MARKET
def calculate_metrics(data):
    returns = data.pct_change().dropna(how = 'all') #Calculate daily returns, skip empty rows
    results = {
        'volatility': returns.std() * np.sqrt(252),
        'sharpe': (returns.mean() * 252 - 0.02) / (returns.std() * np.sqrt(252)),
        'max_drawdown': (data / data.cummax() - 1).min(),
        'cumulative_returns': (returns + 1).cumprod()
    }
    X = returns['^GSPC'].values.reshape(-1, 1) #Fit market returns to the model
    for etf in ['NANC', 'KRUZ', '^GSPC']: #Only run regression for the two bipartisan ETFs and S&P 500
        y = returns[etf].values
        m = LinearRegression().fit(X, y)
        results.update({
            f'{etf}_alpha': m.intercept_,
            f'{etf}_beta': m.coef_[0],
            f'{etf}_r2': m.score(X, y),
            f'{etf}_model': m
        })
    return results


# CONGRESS.GOV SIGNIFICANT EVENTS 
def get_automated_dates(api_key, max_pages=70):
    source = f"https://api.congress.gov/v3/bill?api_key={api_key}&format=json" #Calls API for congress.gov
    events = []
    ticker_idx = 0 #step count
    start_evt = data.index[0]  # first date in the dataset
    end_evt = data.index[-1]   # last date in the dataset
    for page in range(max_pages):
        url = f"{source}&offset={page*250}" #250 bills per page
        request = requests.get(url) 
        if request.status_code != 200:
            print(f"API request failed:{request.status_code}") #Error checking
            break
        
        bills = request.json().get("bills", []) #convert API response from JSON to Python dictionary
        
        for bill in bills:
            date_str = bill.get("latestAction", {}).get("actionDate") or bill.get("updateDate") #Get latest action date or update date
            if not date_str: #Error checking: if no bill is found for this date
                print(f"No recorded bill of this date {date_str}")
                continue #skip to next bill
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
            if not (start_evt <= event_date <= end_evt): #Eroror checking: if event date out of range
                print(f"Event date {event_date} out of range")
                continue #skip to next bill
            
            ticker = ['NANC', 'KRUZ'][ticker_idx % 2] #alternate between the two ETFs only after each step
            ticker_idx += 1 #step count update
            #store event list
            label = bill.get("title", "Untitled Bill")
            events.append({"label": label, "ticker": ticker, "event_date": event_date.strftime("%Y-%m-%d")}) 
    return events

# BACKTEST SIGNIFICANT EVENTS 

def run_automated_event_study(api_key, data, p_thresh=0.05):
    all_events = get_automated_dates(api_key)
    last_date = data.index[-1] #Last date data is recorded
    post_days = 10 #Post-event window (Events too recent might not have enough data and low p-value regardless)
    valid_events = [] #List of valid events

# Filter out events that don't have a full post-event window (full analysis of p-value not available)
    for evt in all_events:
        ev_dt = datetime.strptime(evt['event_date'], "%Y-%m-%d")
        if ev_dt + timedelta(days=post_days) <= last_date:
            valid_events.append(evt)

    print("\n\nSignificant Events (p < 0.05)")
    sig_count = 0
    for evt in valid_events:
        try:
            car, t_stat, p_val = run_event_study(data, evt['ticker'], evt['event_date'])
            if p_val < p_thresh:
                sig_count += 1
                print(f"{evt['label']} ({evt['ticker']} {evt['event_date']}): CAR {car:.2%}, "
                      f"t-stat {t_stat:.2f}, p-value {p_val:.3f} ✅ Significant")
        except Exception: #Error checking
            continue

# Summary of significant events
    total = len(valid_events)
    if total > 0:
        pct = sig_count / total * 100
        print(f"{sig_count}/{total} events significant ({pct:.1f}% of total valid events)")
    else:
        print("No events with a full post-event window to analyze.")

#---------------------------------------------------



#---------------------------------------------------
#  Outputs
# VISUALIZATION 
def plot_performance(data):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    for ax, etf in zip(axes, ['NANC', 'KRUZ']):
        start = pd.to_datetime(get_inception_dates()[etf]) #Start date from inception date
        etf_px = data[etf].loc[start:] #Access ETF data since its inception date
        first = etf_px.first_valid_index() #Valid starting point
        spx_px = data['^GSPC'].loc[first:]  # Get S&P 500 data from the same date
        norm_etf = etf_px / etf_px.loc[first] * 100  # Normalize ETF data
        norm_spx = spx_px / spx_px.loc[first] * 100  # Normalize S&P 500 data
        
        # Plot normalized data
        ax.plot(norm_etf, label=etf)
        ax.plot(norm_spx, '--', label='S&P 500')
        ax.axhline(100, color='black', linestyle='-')  # Baseline at 100%
        
        # Add labels and title
        ax.set_title(f"{etf} vs S&P 500")
        ax.set_xlabel('Date')
        ax.legend()
        ax.grid(True)
    
    # Add a shared y-axis label
    axes[0].set_ylabel('Normalized Value (%)')
    
    plt.tight_layout()
    plt.show()
   
#REGRESSION AND SCATTER PLOT
def plot_regression(results, data):
    returns = data.pct_change().dropna()
    X = returns['^GSPC'].values.reshape(-1, 1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for ax, etf in zip(axes, ['NANC', 'KRUZ']):
        model = results[f'{etf}_model'] #regression model for each ETF
        y = returns[etf].values
        y_pred = model.predict(X)
        
        ax.scatter(X, y, alpha=0.5, label='Daily Returns')
        ax.plot(X, y_pred, color='red', label='Regression Line')
        ax.set_title(f'{etf} vs S&P 500')
        ax.set_xlabel('S&P 500 Returns')
        ax.set_ylabel(f'{etf} Returns')
        ax.legend()
        ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
# MAIN FUNCTION
if __name__ == "__main__":
    print("Starting ETF Analysis...")
    raw = input_data()
    if raw is None:
        print("Data fetch failed. Exiting.") 
        exit() #Error checking: Stop program if data input failed
    
    data = clean_data(raw)
    if data is None:
        print("Data cleaning failed.")
        exit()
    metrics = calculate_metrics(data)
    print(f"\n\nETF Performance Analysis Report")
    print(f"Analysis Period: {data.index[0].date()} to {data.index[-1].date()}")
    for t in ['NANC', 'KRUZ', '^GSPC']: 
        print(f"\n{t} Performance:")
        print(f"Annualized Volatility: {metrics['volatility'][t]:.2%}")
        print(f"Sharpe Ratio: {metrics['sharpe'][t]:.2f}")
        print(f"Max Drawdown: {metrics['max_drawdown'][t]:.2%}")
        print(f"Alpha: {metrics[f'{t}_alpha']:.4f}, Beta: {metrics[f'{t}_beta']:.2f}")
            
    # Single-event study example
    date = choose_date()       
    print(f"\n\nManual Back-test '{date}':")
    for ticker in get_inception_dates().keys():
        if ticker == '^GSPC':
            print("Skipping S&P 500 vs itself")
            continue
        try:
            car, t_stat, p_val = run_event_study(data, ticker, date)
            flag = "✅ Significant" if p_val < 0.05 else "Not significant"
            print(f"{ticker} on '{date}' → CAR {car:.2%}, t-stat {t_stat:.2f}, p-value {p_val:.3f} {flag}")
        except Exception as e:
            print(f"{ticker} error on '{date}': {e}")  

    run_automated_event_study("hNI3oldMUe5knB7iQ7fhftN04Orr5MGlI9a1YgNY", data)
    plot_performance(data)
    plot_regression(metrics, data)
#---------------------------------------------------
