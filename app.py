from dotenv import load_dotenv
load_dotenv()
import json
import praw
import os
import logging
from pathlib import Path
from datetime import datetime
from ai import identify_problems_from_post, label_problem
import argparse

#########################################################
# Settings
#########################################################

curr_dir = Path(__file__).parent
CUSTOM_LOG_LEVEL = 25
logging.addLevelName(CUSTOM_LOG_LEVEL, 'CUSTOM')
def custom(self, message, *args, **kws):
    if self.isEnabledFor(CUSTOM_LOG_LEVEL):
        self._log(CUSTOM_LOG_LEVEL, message, args, **kws)
class CustomLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == CUSTOM_LOG_LEVEL
logging.Logger.custom = custom
# Configure logging settings
logger = logging.getLogger(__name__)
logger.setLevel(CUSTOM_LOG_LEVEL)

parser = argparse.ArgumentParser(description='Find problems in Reddit posts')
parser.add_argument('subreddit', type=str, help='The subreddit to search')
parser.add_argument('industry', type=str, help='The industry to search for problems')
parser.add_argument('--num_posts', type=int, default=10, help='The number of posts to search')
parser.add_argument('--labels', type=str, nargs='+', default=[], help='The existing labels to use for problem labeling')
args = parser.parse_args()

log_file_path = curr_dir / "runs" / args.subreddit / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
# create the directory + file if it doesn't exist
log_file_path.parent.mkdir(parents=True, exist_ok=True)
# Create a handler that writes log messages to a file
log_file = curr_dir / log_file_path
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(CUSTOM_LOG_LEVEL)
file_handler.setFormatter(logging.Formatter('%(message)s'))
file_handler.addFilter(CustomLevelFilter())  # Add the custom filter to the handler

# Add the handler to the logger
logger.addHandler(file_handler)

#########################################################
# Main
#########################################################

reddit = praw.Reddit(
    client_id = os.environ.get("REDDIT_CLIENT_ID"),
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET"),
    password= os.environ.get("REDDIT_PASSWORD"),
    user_agent= os.environ.get("REDDIT_USER_AGENT"),
    username= os.environ.get("REDDIT_USERNAME")
)

def problem_search(subreddit_name, industry, labels=[], num_posts=10):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top(limit=num_posts):
        text = f"# {submission.title}\n\n{submission.selftext}"
        identified_problems = identify_problems_from_post(text, industry, subreddit)
        for problem in identified_problems:
            try:
                problem_labels, new_labels = label_problem(problem, labels, industry)
                labels.extend(new_labels)
                log_item = {
                    "fullname": submission.fullname,
                    "title": submission.title,
                    "text": submission.selftext,
                    "source": submission.url,
                    "problem": problem,
                    "labels": problem_labels
                }
                logger.custom(json.dumps(log_item))
            except ValueError as e:
                continue

problem_search(args.subreddit, args.industry, args.labels, args.num_posts)