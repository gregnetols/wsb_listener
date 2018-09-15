import praw
import re
from datetime import datetime, timedelta
from pymongo import MongoClient
from ProcessComment import process_comment, parse_ticker_symbols, analyze_ticker_comments
from WriteToMongo import write_comment, query_comments, write_hour_ticker_counts
from utilities import read_yml

praw_config = read_yml('praw_config.yml')
reddit = praw.Reddit(client_id=praw_config['client_id'],
                     client_secret=praw_config['client_secret'],
                     password=praw_config['password'],
                     user_agent=praw_config['user_agent'],
                     username=praw_config['username'])
subreddit = reddit.subreddit('wallstreetbets')

mongo_config = read_yml('mongo_config.yml')
client = MongoClient(host=mongo_config['host'],
                     port=mongo_config['port'])
db = client.wallStreetBets


def main():
    then = datetime.now()

    #For testing truncate collection before each run
    db.drop_collection('comments')
    db.drop_collection('hour')

    for comment in subreddit.stream.comments():

        comment_dict = process_comment(comment)
        comment_dict = parse_ticker_symbols(comment_dict)
        #Test
        print(comment_dict['created_utc'])
        #^^^
        write_comment(db, 'comments', comment_dict)

        # Once an hour
        if datetime.now() > then + timedelta(hours=1):
            then = datetime.now()

            ticker_comments = query_comments(db, 'comments')
            ticker_counts = analyze_ticker_comments(ticker_comments)

            write_hour_ticker_counts(db, 'hour', ticker_counts)


if __name__ == '__main__':
    main()
