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


def query_ticker_comments_by_datetime(database, collection, start, end):

    exists = {'tickersPresent': {'$exists': 'true'}}
    time_bounds = {'created_utc': {'$gte': start, '$lt': end}}
    query = {'$and': [exists, time_bounds]}
    print(query)

    results = database[collection].find(query)

    return results


def write_ticker_counts(database, collection, ticker_counts, id_column):

    id_column_value = ticker_counts[id_column]

    database[collection].replace_one({id_column: id_column_value}, ticker_counts, upsert=True)