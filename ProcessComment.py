import re
from datetime import datetime

def process_comment(comment):
    '''

    :param comment:
    :return:
    '''
    comment_dict = {}

    # Basic info
    comment_dict['id'] = comment.id
    comment_dict['created_utc'] = datetime.utcfromtimestamp(comment.created_utc)

    # Comment info
    comment_dict['author_name'] = comment.author.name
    comment_dict['body'] = comment.body

    return comment_dict


def parse_ticker_symbols(comment):
    '''

    :param comment:
    :return:
    '''
    text = comment['body']
    pattern = re.compile('[$][A-Za-z]{1,5}')

    matches = [ticker.upper() for ticker in list(set(pattern.findall(text)))]
    if len(matches) > 0:
        comment['tickersPresent'] = matches

    return comment


def aggregate_ticker_counts(comments, header_data):
    ticker_dict = {}

    for key, value in header_data.items():
        ticker_dict[key] = value

    ticker_dict['tickers'] = {}
    for comment in comments:
        for ticker in comment['tickersPresent']:
            ticker = ticker.replace('$','')
            if ticker not in ticker_dict['tickers'].keys():
                ticker_dict['tickers'][ticker] = 1
            else:
                ticker_dict['tickers'][ticker] = ticker_dict['tickers'][ticker] + 1

    return ticker_dict



