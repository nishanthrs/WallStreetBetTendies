import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import psycopg2

from analytics.get_company_keywords import get_company_most_common_keywords_res
from analytics.get_moving_volatility import get_moving_volatility_res
from analytics.get_tick_data import get_tick_data_from_db
from analytics.get_subreddit_sentiment_disagreement import get_subreddit_sentiment_disagreement_res
from analytics.get_sentiment_popularity_correlation import get_sentiment_popularity_correlation_res
from analytics.sentiment_company import get_sentiment_count_res


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


def get_subreddit_sentiment_disagreement(request):
    try:
        subreddit_name = request.GET['subreddit_name']
        subreddit_name_2 = request.GET['subreddit_name_2']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        query_filename = 'sql_scripts/subreddit_sentiment_disagreement.sql'
        res = get_subreddit_sentiment_disagreement_res(query_filename, subreddit_name, subreddit_name_2, start_date, end_date)
        return JsonResponse({'status': 200, 'res': res})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with getting subreddit sentiment disagreement data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})


def get_sentiment_popularity_correlation(request):
    try:
        subreddit_name = request.GET['subreddit_name']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        query_filename = 'sql_scripts/sentiment_popularity_correlation.sql'
        res = get_sentiment_popularity_correlation_res(query_filename, subreddit_name)
        return JsonResponse({'status': 200, 'res': res})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with getting subreddit sentiment disagreement data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})


def get_moving_volatility(request):
    try:
        stock_symbol = request.GET['stock_symbol']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        res = get_moving_volatility_res(stock_symbol, start_date, end_date)
        return JsonResponse({'status': 200, 'res': res})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with getting moving volatility data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})


def get_sentiment_count(request):
    try:
        company = request.GET['company']
        subreddit_name = request.GET['subreddit_name']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        res = get_sentiment_count_res(company, subreddit_name)
        return JsonResponse({'status': 200, 'res': res})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with getting company sentiment data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})


def get_company_keywords(request):
    try:
        company = request.GET['company']
        subreddit_name = request.GET['subreddit_name']
    except KeyError as e:
        print('Bad client request: ', str(e))
        return JsonResponse({'status': 400, 'error': 'Missing {} param'.format(str(e))})

    try:
        res = get_company_most_common_keywords_res(company, subreddit_name)[subreddit_name]
        return JsonResponse({'status': 200, 'res': res})
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR with getting company sentiment data: ', error)
        return JsonResponse({'status': 404, 'error': str(error)})
    