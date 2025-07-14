import os
import re
import praw
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Setup Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def scrape_reddit_user(username, limit=100):
    user = reddit.redditor(username)
    posts = []
    comments = []

    print(f"[+] Scraping Reddit user: {username}")
    try:
        for submission in tqdm(user.submissions.new(limit=limit), desc="Posts"):
            posts.append(f"Title: {submission.title}\nBody: {submission.selftext}")
        for comment in tqdm(user.comments.new(limit=limit), desc="Comments"):
            comments.append(f"Comment: {comment.body}")
    except Exception as e:
        print("Error fetching user data:", e)

    return posts, comments

def build_prompt(posts, comments, username):
    combined = "\n\n".join(posts + comments)
    prompt = f"""
You are a helpful AI assistant. Your task is to analyze Reddit posts and comments to build a detailed **User Persona** in the following structured format.

Generate:
- Motivations
- Behavior & Habits
- Frustrations
- Goals & Needs
- Personality
- A few demographic guesses (age, occupation, location, status, archetype)

Also **cite** relevant post/comment snippets at the end that helped you form your insights.

--- Example Output Structure ---
User Persona for {username}

- Name: [Generated or guessed name]
- Age: [inferred]
- Occupation: [inferred]
- Status: [e.g., single, married]
- Location: [e.g., city or country]
- Tier: [e.g., Early Adopter, Skeptic]
- Archetype: [e.g., The Creator, The Analyst]

🧠 Personality
- Introvert/Extrovert: [value]
- Thinker/Feeler: [value]
- Judging/Perceiving: [value]
- Any other notable traits...

🎯 Motivations
- [motivation1]
- [motivation2]

📌 Behaviour & Habits
- [pattern 1]
- [pattern 2]

😩 Frustrations
- [pain point 1]
- [pain point 2]

🎯 Goals & Needs
- [goal1]
- [goal2]

📚 Supporting Citations:
- "comment/post text..." → [trait inferred]
- "..." → [...]

Use only the text below to make the inference:
---
{combined}
"""
    return prompt.strip()

def call_together_llm(prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in user research. Based on Reddit posts and comments, "
                    "you will generate a detailed user persona following a UX format. "
                    "Include: Age, Occupation, Location, Status, Motivations, Frustrations, "
                    "Behavior, Goals, Personality (MBTI-style), and cited comments."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        print("❌ Chat API error:\n", response.text)
        return "[ERROR] Chat API failure"


def save_output(username, content):
    os.makedirs("output", exist_ok=True)
    file_path = f"output/{username}_persona.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Saved persona to {file_path}")

def extract_username(url):
    match = re.search(r'reddit\.com/user/([^/]+)/?', url)
    return match.group(1) if match else None

def main():
    url = input("Enter Reddit profile URL: ").strip()
    username = extract_username(url)
    if not username:
        print("❌ Invalid Reddit profile URL.")
        return

    posts, comments = scrape_reddit_user(username, limit=25)
    if not posts and not comments:
        print("❌ No data found for user.")
        return

    prompt = build_prompt(posts, comments, username)
    persona = call_together_llm(prompt)
    save_output(username, persona)

if __name__ == "__main__":
    main()
# This script is designed to scrape a Reddit user's posts and comments,
# build a detailed user persona using the Together AI API, and save the output.