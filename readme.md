# Set-up

First, you must have an OpenAI API key, to create one, go here:
https://platform.openai.com/account/api-keys

Second, you must have a reddit account, with a script account / app credentials, to create one, go here:
https://www.reddit.com/prefs/apps/

Lastly, open python/run-miner.py and replace the open_ai_key, reddit_credentials with your own data.


# How to use

## Step 1 - activate the virtual environment and install dependencies by running following 3 commands

```
cd python
pipenv install
pipenv shell
```

## Step 2 - Replace the variables in the run-miner.py file with your own data

- *search_queries* - the topics you want to search for (posts the AI finds will be around these topics)
- *max_posts* - the maximum number of posts to analyse
- *qualifier_prompt* - the prompt to use to determine if a post qualifies - this can be whatever you want (eg: does this post contain a business idea, does this post contain a user problem, etc)
- *generation_prompt* - the prompt to use for generation - this can be whatever you want (eg: translate the post to spanish, create a short summary of the post, create a TikTok script, ...)

## Step 3 - Run the miner
```
python run-miner.py
```

## Step 4 - Get the CSV

The CSV will be saved in the python/exports folder, with the name being your project name combined with the date.

-- 

Note: this software is provided as is, without any guarantees. Use at your own risk.