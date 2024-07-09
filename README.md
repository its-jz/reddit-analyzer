#reddit-analyzer

## Todos
1. Make sure the number of tags is not too high (it will be hard for chatbot to handle)

This tool analyzes a subreddit on a specific industry. It will read the top 1000 posts and comments and identify
1. potential problems that people are facing in the industry
2. key concepts ***todo***
3. reddit users who are ***todo***
    - knowledgeable in the industry, or
    - have a problem


## Pre-requisites
- Reddit API credentials 
    1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
    2. Click on "Create App" or "Create Another App".
    3. Fill in the details:
        - App name: Choose a name for your app.
        - App type: Select "script" for personal use or "installed app" for mobile/desktop apps.
        - Description: Optional.
        - About URL: Optional.
        - Redirect URI: For scripts, you can use http://localhost:8000 or any other URI. For web apps, provide your web app's URL.  
    4. Get Your Credentials:
- OpenAI API key

## How to use
1. create virtual environment and install requirements
2. copy `.env.example` to `.env` and fill in the credentials
3. run `python app.py [-h] [--num_posts NUM_POSTS] [--labels LABELS [LABELS ...]] subreddit industry`
    - `subreddit` is the name of the subreddit you want to analyze
    - `industry` is the industry you want to analyze
    - `--num_posts` is the number of posts to analyze. Default is 10
    - `--labels` are the labels you want to use to identify the industry. Default is `['industry']`
    The result will be saved in `runs/` folder
4. run 'python read.py' to read the result in a streamlit app

