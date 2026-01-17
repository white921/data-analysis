import requests
import pandas as pd
from datetime import datetime, timedelta
from config import (
    GITHUB_TOKEN,
    LANGUAGES,
    REPOS_PER_LANGUAGE,
)

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# 現在データ用
now_end = datetime.utcnow()
now_start = now_end - timedelta(days=30)

# 過去データ用
past_end = now_end - timedelta(days=365 * 3)
past_start = past_end - timedelta(days=30)

def get_repositories(language, n):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": n
    }
    res = requests.get(url, headers=HEADERS, params=params)
    res.raise_for_status()
    return res.json()["items"]


def get_commit_count(full_name, start_date, end_date):
    url = f"https://api.github.com/repos/{full_name}/commits"
    params = {
        "since": start_date.isoformat() + "Z",
        "until": end_date.isoformat() + "Z",
        "per_page": 100
    }

    res = requests.get(url, headers=HEADERS, params=params)
    if res.status_code != 200:
        return 0

    return len(res.json())

def main():
    rows = []

    for language in LANGUAGES:
        repos = get_repositories(language, REPOS_PER_LANGUAGE)

        for repo in repos:
            # 今
            rows.append({
                "language": language,
                "period": "recent",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "issues": repo["open_issues_count"],
                "commits": get_commit_count(
                    repo["full_name"],
                    now_start,
                    now_end
                )
            })

            # 昔（3年前）
            rows.append({
                "language": language,
                "period": "past",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "issues": repo["open_issues_count"],
                "commits": get_commit_count(
                    repo["full_name"],
                    past_start,
                    past_end
                )
            })

    df = pd.DataFrame(rows)
    df.to_csv("data/raw_github_data.csv", index=False)
    print("Saved: data/raw_github_data.csv")


if __name__ == "__main__":
    main()
