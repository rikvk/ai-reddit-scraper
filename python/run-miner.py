from app.main import run_miner

open_ai_key = "" # your open ai key

reddit_credentials = {
    "client_id": "",
    "client_secret": "",
    "password": "",
    "user_agent": "",
    "username": ""
}

# Give your project a name (only alphanumeric characters)
# Note, if you use the same name your previous data will be overwritten
project_name = "MyProject" # your project name (only alphanumeric characters)

# Define the list of search queries
search_queries = ["AI", "GPT", "Generative AI", "AI Chatbot", "AI Agent", "AI Assistant", "AI Automation"]

# Max posts to analyse
max_posts = 100

# Qualifier Prompt
qualifier_prompt = """
The post contains a problem, idea, question or something around which a TikTok can be created.

When to say TRUE:
- The post asks a question based on which we could create a TikTok with an answer.
- The post highlights a cool advancement which we could feature in a TikTok.
- The post highlights a cool tool we can highlight in a TikTok.
- The post proposes a cool idea or solution which we could feature in a TikTok.
"""

# Generation Prompt (will run if qualifier_prompt is true)
generation_prompt = """
Based on this reddit post, generate 2 things for me:
- A short summary of a viral TikTok idea.
- The hook to open the video.

My TikTok style is generally informative and to the point, no skits or memes. Just featuring cool things, highlighting cool advancements, or posing intersting questions.
"""



run_miner(open_ai_key, reddit_credentials, project_name, search_queries, max_posts, qualifier_prompt, generation_prompt)



