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
    comment_dict['created_utc'] = datetime.fromtimestamp(comment.created_utc)
    comment_dict['created'] = datetime.fromtimestamp(comment.created)

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
    pattern = re.compile('[$][A-Za-z][\S]*')

    matches = list(set(pattern.findall(text)))
    if len(matches) > 0:
        comment['tickersPresent'] = matches

    return comment


def analyze_ticker_comments(comments, beg_last_hour):
    '''

    :param comments:
    :return:
    '''
    ticker_dict = {}
    ticker_dict['start_hour'] = beg_last_hour

    pattern = re.compile('[[A-Za-z]{1,6}')
    for comment in comments:
        for ticker in comment['tickersPresent']:
            ticker = pattern.findall(ticker)[0]
            if ticker not in ticker_dict.keys():
                ticker_dict[ticker] = 1
            else:
                ticker_dict[ticker] = ticker_dict[ticker] + 1

    return ticker_dict
