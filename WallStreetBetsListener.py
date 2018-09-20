import praw
import re
from datetime import datetime, timedelta
from pymongo import MongoClient
from ProcessComment import process_comment, parse_ticker_symbols, aggregate_ticker_counts
from WriteToMongo import write_comment, query_ticker_comments_by_datetime, write_ticker_counts
from utilities import read_yml, new_hour, new_day


praw_config = read_yml("praw_config.yml")
reddit = praw.Reddit(client_id=praw_config['client_id'],
                     client_secret=praw_config['client_secret'],
                     password=praw_config['password'],
                     user_agent=praw_config['user_agent'],
                     username=praw_config['username'])
subreddit = reddit.subreddit('wallstreetbets')

mongo_config = read_yml("mongo_config.yml")
client = MongoClient(host=mongo_config['host'],
                     port=mongo_config['port'])
db = client.wallStreetBets


def main():
    current_hour = datetime.now().hour
    current_day = datetime.now().day

    #For testing truncate collection before each run
    #db.drop_collection('comments')
    #db.drop_collection('hour')

    for comment in subreddit.stream.comments():

        comment_dict = process_comment(comment)
        comment_dict = parse_ticker_symbols(comment_dict)
        write_comment(db, 'comments', comment_dict)

        # Once an hour
        if new_hour(current_hour):
            current_hour = datetime.now().hour

            beg_last_hour = (datetime.utcnow() - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            end_last_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

            ticker_comments = query_ticker_comments_by_datetime(db, 'comments', beg_last_hour, end_last_hour)

            header_data = {'start_hour': beg_last_hour, 'end_hour': end_last_hour}
            ticker_counts = aggregate_ticker_counts(ticker_comments, header_data)

            write_ticker_counts(db, 'hour', ticker_counts, 'start_hour')



        if new_day(current_day):
            current_day = datetime.now().day

            beg_yesterday = (datetime.utcnow() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

            ticker_comments = query_ticker_comments_by_datetime(db, 'comments', beg_yesterday, end_yesterday)

            header_data = {'date_gte': beg_yesterday, 'date_lt': end_yesterday}
            ticker_counts = aggregate_ticker_counts(ticker_comments, header_data)

            write_ticker_counts(db, 'day', ticker_counts, 'date')




if __name__ == '__main__':
    main()
