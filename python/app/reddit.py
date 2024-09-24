import praw
import prawcore
# Function that creates reddit client
def init_reddit(reddit_credentials):
    return praw.Reddit(
        client_id=reddit_credentials['client_id'],
        client_secret=reddit_credentials['client_secret'],
        password=reddit_credentials['password'],
        user_agent=reddit_credentials['user_agent'],
        username=reddit_credentials['username'],
    )