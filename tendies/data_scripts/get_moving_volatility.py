import collections
import datetime
import json
import requests
from string import printable
import sys
import urllib

sys.path.append('..')
import db_helpers


def get_moving_volatility_res(stock_symbol, start_date, end_date):
    conn = db_helpers.connect_to_db()
    cur = conn.cursor()

    cur.callproc('calVolatility2', ['1999-11-01 00:00:00', '2001-12-07 00:00:00'])
    conn.commit()

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    res = cur.fetchall()
    final_res = []
    for row in res:
        row = row[0]
        curr_stock_symbol = row['stock_symbol']
        timestamp = datetime.datetime.strptime(row['ts'], '%Y-%m-%d %H:%M:%S')
        if curr_stock_symbol == stock_symbol and timestamp >= start_date and timestamp <= end_date:
            final_res.append(row)
    
    return final_res
