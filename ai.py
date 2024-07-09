import tiktoken
from openai import OpenAI
import json
client = OpenAI()
model="gpt-4o"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def identify_problems_from_post(post, industry, subreddit):
    """Return a list of problems as a list of strings from the post."""
    system_msg = (
        f"You are a world-class expert in the **{industry}** industry, highly adept at identifying industry-specific problems. "
        f"You will be given a post from the **r/{subreddit}** subreddit. "
        "The poster might be complaining, asking for advice, sharing a story, or asking a question. "
        "Your task is NOT to answer the question or respond to the post. Instead, you must identify "
        "the pain points or problems in the given industry that the post is highlighting.\n\n"
        "For example, if the post says, \"Real estate agent is not responding to my calls. "
        "What should I do?\", the identified problem could be \"It is hard for real estate "
        "agents to respond to clients in a timely manner.\"\n\n"
        "Respond with a numbered list in markdown format, like this:\n\n"
        "1. Problem 1\n"
        "2. Problem 2\n"
        "3. Problem 3\n"
        "...\n\n"
        "When identifying problems, follow these guidelines:\n"
        "- Problems have to be industry-specific. If a problem is too general, ignore it.\n"
        "- Problems should be important to the industry. If a problem is trivial, ignore it.\n"
        "- Problems should be based on the post content. Do not make assumptions.\n"
        "- If a post contains multiple problems, list them all.\n"
        "- If a post does not contain any problems, say \"NOT_FOUND\".\n"
        "- List at most 3 problems per post.\n\n"
        
    )
    
    # print("Input tokens:", num_tokens_from_string(system_msg, "cl100k_base"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": post}
        ]
    )
    if 'NOT_FOUND' in response.choices[0].message.content:
        return []
    # return problem without the markdown numbering
    problems = response.choices[0].message.content.split("\n")
    problems = [p[3:].strip() for p in problems if p]
    return problems

def label_problem(problem, existing_labels, industry):
    example_response = {
        "problem_labels": ["Home Inspection", "House Flipping", "Leads Generation"],
        "new_labels": ["Leads Generation"]
    }
    system_msg = ("You are a world-class categorizer who is extremely keen on categorizing problems "
                    "in the " + industry + " industry. Your task is to label the problem using domain-specific "
                    "categories. You are given a problem statement and an optional list of existing "
                    "labels. Label the problem with up to 3 categories from the list when possible. "
                    "If, on top of the existing labels, you find a new category that fits the problem, "
                    "add it to the list of new labels. Return the list of problem labels and the new labels "
                    "in json format. For example:\n\n" + json.dumps(example_response))
    
    response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": "existing_labels: \n" + json.dumps(existing_labels)},
            {"role": "user", "content": "problem: \n" + problem},   
        ]
    )
    
    res = response.choices[0].message.content
    res = json.loads(res)
    if "problem_labels" not in res or "new_labels" not in res:
        raise ValueError("The response from the model is not in the correct")
    return res["problem_labels"], res["new_labels"]
    
    
    

    

