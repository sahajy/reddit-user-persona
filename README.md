# Reddit User Persona Generator

This project scrapes Reddit user activity and uses a large language model via Together.ai to generate a detailed **user persona** — including motivations, behavior, frustrations, goals, and personality traits — with **citations from actual posts/comments**.

# Features

- ✅ Input: Reddit user profile URL
- ✅ Scrapes both **posts and comments**
- ✅ Builds a full persona using **Together AI's LLM**
- ✅ Outputs results in `.txt` files under `output/`
- ✅ Each persona attribute includes **citations** from the user's activity

## Example Use Case

Input:


[https://www.reddit.com/user/kojied/](https://www.reddit.com/user/kojied/)


Output:

output/kojied\_persona.txt


## 🛠️ Technologies Used

- [Python](https://www.python.org/)
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/)
- [Together.ai API](https://docs.together.ai/)
- `dotenv`, `tqdm`, `requests`


##  How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/sahajy/reddit-user-persona.git
cd reddit-user-persona
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file in the project root with the following format:

```env
TOGETHER_API_KEY=your_together_api_key
REDDIT_CLIENT_ID=your_reddit_app_client_id
REDDIT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=script:reddit-persona-builder:v1.0 (by u/your_reddit_username)
```

 **This file is excluded from Git using `.gitignore`**

---

### 4. Run the Script

```bash
python reddit_persona.py
```

When prompted, paste a Reddit profile URL:

```
https://www.reddit.com/user/Hungry-Move-6603/
```

---

## 📂 Output Files

Generated persona files are saved in the `output/` directory:

```
output/
├── kojied_persona.txt
├── Hungry-Move-6603_persona.txt
```

Each file includes:

* Name, Age, Occupation (guessed)
* Personality Type (MBTI-style)
* Motivations, Frustrations, Goals
* ✅ Supporting citations from actual Reddit comments/posts

---

## 📋 Project Structure

```
reddit-user-persona/
├── reddit_persona.py
├── requirements.txt
├── .env               ← not committed
├── .gitignore
├── output/
│   ├── kojied_persona.txt
│   └── Hungry-Move-6603_persona.txt
└── README.md
```

---

##  Notes

* Make sure your `.env` file is properly configured with valid API keys.
* Only public Reddit profiles can be scraped.
* The project adheres to [PEP-8](https://peps.python.org/pep-0008/) style guidelines.

---

## Contact

If you'd like to get in touch about this project, feel free to connect via GitHub(https://github.com/sahajy) or LinkedIn (https://www.linkedin.com/in/sahaj-yadav-070b9930a/) or GMail(sahajy330@gmail.com).

---

##  Acknowledgments

This project was created as part of an assignment for the AI/LLM Engineer Intern position at **BeyondChats**.

````

---

Once you've added this:

1. In VS Code:
   - Right-click in the root folder → New File → `README.md`
   - Paste all the above text
   - Save

2. Then in terminal:

```bash
git add README.md
git commit -m "Add full README with setup and usage instructions"
git push
````

