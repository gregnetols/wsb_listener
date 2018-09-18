from datetime import datetime, timedelta

def write_comment(database, collection, comment):
    '''

    :param database:
    :param collection:
    :param comment:
    :return:
    '''

    comment_id = comment['id']

    database[collection].replace_one({'id':comment_id}, comment, upsert=True)

def write_hour_ticker_counts(database, collection, ticker_counts):
    '''

    :param database:
    :param collection:
    :param ticker_counts:
    :return:
    '''
    start_hour = ticker_counts['start_hour']
    database[collection].replace_one({'start_hour': start_hour}, ticker_counts, upsert=True)


def write_day_ticker_counts(database, collection, ticker_counts):

    date = ticker_counts['date']
    database[collection].replace_one({'date': date}, ticker_counts, upsert=True)


def query_comments(database, collection):
    '''

    :return:
    '''
    beg_last_hour = (datetime.utcnow() - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    end_last_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    print('beg_last_hour ---', beg_last_hour)
    print('end_last_hour ---', end_last_hour)

    exists = {'tickersPresent': {'$exists':'true'}}
    time_bounds = {'created_utc': {'$gte': beg_last_hour,'$lt': end_last_hour}}
    query = {'$and': [exists, time_bounds]}
    print(query)

    results = database[collection].find(query)

    return results, beg_last_hour, end_last_hour


def query_comments_day(database, collection):

    beg_yesterday = (datetime.utcnow() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    print('beg_yesterday ---', beg_yesterday)
    print('end_yesterday ---', end_yesterday)

    exists = {'tickersPresent': {'$exists':'true'}}
    time_bounds = {'created_utc': {'$gte': beg_yesterday,'$lt': end_yesterday}}
    query = {'$and': [exists, time_bounds]}
    print(query)

    results = database[collection].find(query)

    return results, beg_yesterday

