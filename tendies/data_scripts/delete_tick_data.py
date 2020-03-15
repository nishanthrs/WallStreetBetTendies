import collections
import datetime
import json
import requests
import sys
import urllib

sys.path.append('..')
import db_helpers


def delete_tick_data_from_db(stock_symbol, start_date, end_date):
    conn = db_helpers.connect_to_db()
    cur = conn.cursor()

    delete_stock_tick_data_query = (
        'DELETE FROM StockTickData WHERE stock_symbol=\'{}\''
        'AND ts::DATE >= DATE \'{}\' AND ts <= DATE \'{}\''.format(
            stock_symbol, start_date, end_date
        )
    )
    cur.execute(delete_stock_tick_data_query)
    conn.commit()

    cur.close()
