import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import psycopg2

# from ..data_scripts.populate_stock_tick_data import load_tick_data, upload_to_db

from data_scripts.populate_stock_tick_data import load_tick_data, upload_to_db
from data_scripts.delete_tick_data import delete_tick_data_from_db
from data_scripts.get_tick_data import get_tick_data_from_db

def get_stock_tick_data(request):
    try:
        stock_symbol = request.GET['stock_symbol']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
    except KeyError as e:
        print('Request does not have required params: ', str(e))

    closing_prices = get_tick_data_from_db(stock_symbol, start_date, end_date)
    closing_prices['status'] = 200

    return JsonResponse(closing_prices)


def delete_stock_tick_data(request):
    try:
        stock_symbol = request.GET['stock_symbol']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        delete_tick_data_from_db(stock_symbol, start_date, end_date)
        return JsonResponse({'status': 200})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with deleting tick data: {}'.format(error))
        return JsonResponse({'status': 404, 'error': str(error)})


def insert_stock_tick_data(request):
    try:
        stock_symbol = request.GET['stock_symbol']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        tick_data = load_tick_data([stock_symbol])
        upload_to_db(tick_data)
        return JsonResponse({'status': 200})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with uploading tick data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})