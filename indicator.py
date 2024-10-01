
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from stockstats import StockDataFrame as sdf
# import pmdarima as pm



import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# CONFIG:
# period = “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
# interval = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
btc= yf.Ticker("BTC-USD")
btc_usd_90Days = btc.history(period="3mo", interval="1d")
btc_usd_30Days = btc.history(period="1mo", interval="1d")
btc_usd_30Days_Copy = btc_usd_30Days.copy()
stock = sdf.retype(btc_usd_30Days)
# print(btc_usd_90Days)


def closeData():
    return str(btc_usd_90Days['Close'].iloc[-1])


### №1 - rolling window (RW)
def rolling_window():
    rol_RW = btc_usd_90Days['Close'].rolling(window=90, center=False).mean()
    # print('Стратегия №1', 'купить' if btc_usd_90Days['Close'].iloc[-1] > rol_RW.iloc[-1] else 'продать')
    return 'Стратегия №1: ' + ('купить' if btc_usd_90Days['Close'].iloc[-1] > rol_RW.iloc[-1] else 'продать')

### №2 - simple moving average strategy (SMA)
def simple_moving_average():
    rol_SMA_1 = btc_usd_90Days['Close'].rolling(window=45, center=False).mean()
    rol_SMA_2 = btc_usd_90Days['Close'].rolling(window=90, center=False).mean()

    # print('Стратегия №2', 'купить' if rol_SMA_1.iloc[-1] > rol_SMA_2.iloc[-1] else 'продать')
    return 'Стратегия №2: ' +('купить' if rol_SMA_1.iloc[-1] > rol_SMA_2.iloc[-1] else 'продать')

### №3 - exponentially weighted moving average strategy (EWMA)
def exponentially_weighted_moving_average():
    rol_EWMA_1 = btc_usd_90Days['Close'].ewm(span=5, adjust=True, ignore_na=True).mean()
    rol_EWMA_2 = btc_usd_90Days['Close'].ewm(span=30, adjust=True, ignore_na=True).mean()
    # print('Стратегия №3', 'купить' if rol_EWMA_1.iloc[-1] > rol_EWMA_2.iloc[-1] else 'продать')
    return 'Стратегия №3: ' + ('купить' if rol_EWMA_1.iloc[-1] > rol_EWMA_2.iloc[-1] else 'продать')

### №4 - RSI strategy
def relative_strength_index():
    # stock = sdf.retype(btc_usd_30Days)
    rol_RSI = stock['rsi_14'] # в книге rsi_12
    rol_RSI_result = 'ничего'
    # print('BTC-USD 30Days RSI:', rol_RSI.iloc[-1])
    if rol_RSI.iloc[-1] > 70: # в книге > 90
        rol_RSI_result = 'продать'
    elif rol_RSI.iloc[-1] < 30: # в книге < 10
        rol_RSI_result = 'купить'
    # print('Стратегия №4', rol_RSI_result)
    return 'Стратегия №4: ' + rol_RSI_result

### №5 - MACD strategy
def moving_average_convergence_divergence():
    # stock = sdf.retype(btc_usd_30Days)
    signal = stock['macds']
    macd = stock['macd']
    rol_MACD_result = 'ничего'
    # print('BTC-USD 30Days MACD:', macd.iloc[-1])
    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        rol_MACD_result = 'купить'
    elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
        rol_MACD_result = 'продать'
    return 'Стратегия №5: ' + rol_MACD_result

### №6 - RSI and MACD strategy
def rsi_and_macd():
    # stock = sdf.retype(btc_usd_30Days)
    rsi = stock['rsi_12']
    signal = stock['macds']
    macd = stock['macd']
    rol_RSI_MACD_result = 'ничего'
    # print('BTC-USD 30Days RSI:', rsi.iloc[-1])
    if rsi.iloc[-1] < 50 and macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        rol_RSI_MACD_result = 'купить'
    elif rsi.iloc[-1] > 50 and macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
        rol_RSI_MACD_result = 'продать'
    # print('Стратегия №6', rol_RSI_MACD_result)
    return 'Стратегия №6: ' + rol_RSI_MACD_result


### №7 - Triple exponential average strategy
def triple_exponential_average():
    # stock = sdf.retype(btc_usd_30Days)
    rol_TRIX = stock['trix_15']
    rol_TRIX_result = 'ничего'
    if rol_TRIX.iloc[-1] > 0 and rol_TRIX.iloc[-2] < 0:
        rol_TRIX_result = 'продать'
    elif rol_TRIX.iloc[-1] < 0 and rol_TRIX.iloc[-2] > 0:
        rol_TRIX_result = 'купить'
    # print('Стратегия №7', rol_TRIX_result)
    return'Стратегия №7: ' + rol_TRIX_result


### №8 - Williams %R strategy
def williams_percent_r():
    # stock = sdf.retype(btc_usd_30Days)
    rol_Williams = stock.get('wr_6')
    rol_Williams_result = 'ничего'
    if rol_Williams.iloc[-1] < 10:
        rol_Williams_result = 'продать'
    elif rol_Williams.iloc[-1] > 90:
        rol_Williams_result = 'купить'
    # print('Стратегия №8', rol_Williams_result)
    return 'Стратегия №8: ' + rol_Williams_result

########## Learning mean-reversion strategy ####################

### №9 - bollinger bands strategy
def bollinger_bands():
    # print(btc_usd_30Days['Close'])
    middle_base_line = btc_usd_30Days_Copy['Close'].mean()
    std_line = btc_usd_30Days_Copy['Close'].std()
    upper_band = middle_base_line + std_line * 2
    lower_band = middle_base_line - std_line * 2

    rol_BB_result = 'ничего'
    if btc_usd_30Days_Copy['Close'].iloc[-1] < lower_band:
        rol_BB_result = 'купить'
    elif btc_usd_30Days_Copy['Close'].iloc[-1] > upper_band:
        rol_BB_result = 'продать'
    # print('Стратегия №9', rol_BB_result)
    return 'Стратегия №9: ' + rol_BB_result



### #10 - pairs trading strategy

########## Learning mathematical model-based strategies ####################

### №11 - minimization of the portfolio volatility strategy with monthly trading

### №12 - maximum sharpe ratio strategy with monthly trading

########## Learning time-series prediction-based strategies ####################

### №13 - SARIMAX strategy
def sarimax():
    try:
        model = pm.auto_arima(btc_usd_90Days['Close'], seasonal=True)
        forecast = model.predict(7)
        rol_SARIMAX_result = 'ничего'
        if btc_usd_90Days['Close'].iloc[-1] > forecast[-1]:
            rol_SARIMAX_result = 'продать'
        else:
            rol_SARIMAX_result = 'купить'
        print('Стратегия №13', rol_SARIMAX_result)
    except:
        print('Ошибка в стратегии №13')

### #14 - Prophet strategy
def prophet():
    price_df = pd.DataFrame({'y': btc_usd_90Days['Close']}).rename_axis('ds').reset_index()
    price_df['ds'] = price_df['ds'].dt.tz_convert(None)

    model = pm.Prophet()
    model.fit(price_df)
    forecast = model.make_future_dataframe(periods=7, freq='D')
    df_forecast = model.predict(df_forecast)

    last_price = btc_usd_90Days['Close'].iloc[-1]
    forecast_lower = df_forecast['yhat_lower'].iloc[-1]
    forecast_upper = df_forecast['yhat_upper'].iloc[-1]

    
    rol_PROPHET_result = 'ничего'
    if last_price < forecast_lower:
        rol_PROPHET_result = 'купить'
    elif last_price > forecast_upper:
        rol_PROPHET_result = 'продать'
    print('Стратегия №9', rol_PROPHET_result)

# rolling_window()
# simple_moving_average()
# exponentially_weighted_moving_average()
# relative_strength_index()
# moving_average_convergence_divergence()
# rsi_and_macd()
# triple_exponential_average()
# williams_percent_r()
# bollinger_bands()
# sarimax()
# prophet()
