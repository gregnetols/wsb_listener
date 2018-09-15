import praw
import re
from datetime import datetime, timedelta
from pymongo import MongoClient
from ProcessComment import process_comment, parse_ticker_symbols, analyze_ticker_comments
from WriteToMongo import write_comment, query_comments, write_hour_ticker_counts


reddit = praw.Reddit(client_id='ATOrE1YORdowCA',
                     client_secret='0QDTt2o9we6pOINOVIr_pzaPFF0',
                     password='greg211366',
                     user_agent='PrawTime_Streaming',
                     username='PrawTime')
subreddit = reddit.subreddit('wallstreetbets')

client = MongoClient('localhost', 27017)
db = client.wallStreetBets


def main():
    then = datetime.now()

    #For testing truncate collection before each run
    db.drop_collection('comments')
    db.drop_collection('hour')

    for comment in subreddit.stream.comments():

        comment_dict = process_comment(comment)
        comment_dict = parse_ticker_symbols(comment_dict)
        write_comment(db, 'comments', comment_dict)

        # Once an hour
        if datetime.now() > then + timedelta(hours=1):
            then = datetime.now()

            ticker_comments = query_comments(db, 'comments')
            ticker_counts = analyze_ticker_comments(ticker_comments)

            write_hour_ticker_counts(db, 'hour', ticker_counts)


if __name__ == '__main__':
    main()

