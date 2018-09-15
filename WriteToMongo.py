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


def query_comments(database, collection):
    '''

    :return:
    '''
    beg_last_hour = (datetime.now().replace(minute=0, second=0, microsecond=0) -timedelta(hours=1))
    end_last_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

    results = database[collection].find( { '$and': [ {'tickersPresent': {'$exists':'true'}}, {'created': {'$gte': beg_last_hour,'$lt': end_last_hour}} ] } )

    return results, beg_last_hour
