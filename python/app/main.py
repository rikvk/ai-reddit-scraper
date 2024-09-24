import datetime
from app.reddit import init_reddit
from app.database import create_server_connection, execute_query, check_if_submission_already_in_db, export_database_to_csv
import prawcore

from openai import OpenAI


def run_miner(open_ai_key, reddit_credentials, project_name, search_queries, max_posts = 100000, qualifier_prompt = "", generation_prompt = ""):

    # Initialize PRAW with your Reddit application credentials
    reddit = init_reddit(reddit_credentials)

    # create SQLite connection
    connection = create_server_connection(project_name)

    post_count = 0

    try:
        for search_query in search_queries:
            posts = reddit.subreddit('all').search(query=search_query, limit=100)
            # Search for posts with each query in the list
            for submission in posts:
                

                # Stop if we've reached the max posts
                if post_count >= max_posts:
                    break

                post_summary = f"""
---- POST SUMMARY ----
Title: {submission.title}\nURL: {submission.url}
ID: {submission.id}\nSubreddit: {submission.subreddit}
Selftext: {submission.selftext}\n
Created: {submission.created}
----

    """
                print(post_summary)

                # Prepare the data for insertion
                origin = 'reddit'
                external_id = submission.id
                title = submission.title.replace("'", "''")
                external_url = submission.url
                external_subreddit = str(submission.subreddit)
                content = submission.selftext.replace("'", "''")
                external_created = datetime.datetime.fromtimestamp(submission.created)

                if check_if_submission_already_in_db(connection, submission.id, project_name):
                    print("already exists")
                    continue

                qualified = run_qualifier(post_summary, qualifier_prompt, open_ai_key)
                print(f"qualified: {qualified}")
                if qualified == "TRUE":
                    generation = run_generation(post_summary, generation_prompt, open_ai_key)
                    print(f"generation: {generation}")
                    # Prepare your insert query using placeholders
                    insert_query = f"""
                        INSERT INTO {project_name} (
                            origin, external_id, title, external_url, external_subreddit, content, meets_qualifier, generation, external_created, date_created, date_updated
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'));
                    """

                    # Create a tuple of values to insert
                    values_to_insert = (
                        origin, external_id, title, external_url, external_subreddit, content,
                        qualified, generation, external_created
                    )

                    # Execute the query with the values
                    execute_query(connection, insert_query, values_to_insert)
                    print("inserted post")
                
                post_count += 1

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            export_database_to_csv(connection, project_name)
            connection.close()
            print(f"SQLite connection is closed, csv has been generated at exports/{project_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        return True
    return False



def run_qualifier(post_summary, qualifier_prompt, open_ai_key):

    client = OpenAI(api_key=open_ai_key)


    sys = f"""
You are a helpful assistant.
    
You analyse if a reddit post meets a certain criteria.
You return TRUE if it does, FALSE if it doesn't.
ONLY RETURN "TRUE" or "FALSE" (NO QUOTES)

This is the qualifier prompt, check if the post meets it:
{qualifier_prompt}
"""


    # generate some SEO copy here
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": f"""
            #POST TO ANALYSE
            {post_summary} 
            """}
        ]
    )

    return completion.choices[0].message.content

def run_generation(post_summary, generation_prompt, open_ai_key):
    
    client = OpenAI(api_key=open_ai_key)

    sys = f"""You are a helpful assistant."""
    # generate some SEO copy here
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": f"""
            #Instructions
            I need you to do the following generation, based on a reddit post, respond ONLY with the generation:
            {generation_prompt}

            #POST TO ANALYSE
            {post_summary} 
            """}
        ]
    )

    return completion.choices[0].message.content