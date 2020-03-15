import collections
import datetime
import json
import psycopg2
import requests
import sys
import urllib

sys.path.append('..')
import db_helpers

def get_tick_data_from_db(stock_symbol, start_date, end_date):
    conn = db_helpers.connect_to_db()
    cur = conn.cursor()

    get_stock_tick_data_query = (
        'SELECT ts, close_price FROM StockTickData WHERE stock_symbol = \'{}\''
        ' AND ts::DATE >= DATE \'{}\' AND ts <= DATE \'{}\''
        ' ORDER BY ts ASC'.format(stock_symbol, start_date, end_date)
    )

    print('Query to retrieve tick data: ', get_stock_tick_data_query)

    closing_prices = {stock_symbol: []}

    cur.execute(get_stock_tick_data_query)
    conn.commit()

    for ts, close_price in cur:
        price_at_time = {'date': ts, 'close_price': close_price}
        closing_prices[stock_symbol].append(price_at_time)

    cur.close()

    return closing_prices
