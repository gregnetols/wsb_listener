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
    database[collection].insert_one(ticker_counts)


def query_comments(database, collection):
    '''

    :return: 
    '''

    return database[collection].find({'tickersPresent': {'$exists':'true'}})
